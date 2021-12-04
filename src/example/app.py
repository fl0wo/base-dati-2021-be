import json
import uuid
import jwt
import datetime
from functools import wraps

from flask import current_app, flash, \
    jsonify, make_response, redirect, request, \
    url_for

from flask_cors import CORS

from . import app, database

from .models import Cats, Users, Slots, Reservations, \
    WeightRoomReservations

from .security import admin_required, \
    get_current_user, \
    get_current_manager, is_logged, has_role, \
    ADMIN, MANAGER, CUSTOMER, TRAINER, register_user

from .response import Response, DATE_FORMAT, \
    DATE_FORMAT_IN, TIME_FORMAT

from werkzeug.security import generate_password_hash, \
    check_password_hash  # not constant due to salt adding (guarda rainbow table attack)

from .controllers.user_controller import \
    parse_me, update_me, parse_my_res, users_all

from .controllers.slot_controller import \
    parse_slots, add_slot_reservation, add_slot

from .controllers.lesson_controller import \
    parse_lessons

USER_NOT_LOGGED = jsonify({'message': 'user not logged'}), 401
USER_NOT_AUTHORIZED = jsonify({'message': 'user not authorized'}), 401

CORS(app)

basicHeaders = [
    ('Content-Type', 'application/json'),
    ('Access-Control-Allow-Origin', '*'),
    ('Access-Control-Allow-Headers', 'Authorization, Content-Type'),
    ('Access-Control-Allow-Methods', 'POST'),
]


def sendResponse(payload, msg, status):
    r = Response()
    r.data = payload
    r.message = msg
    r.status = status
    return jsonify(r.toJSON()), status, basicHeaders


def doFinallyCatch(do, success, catch):
    try:
        do()
    except :
        return catch
    return success


def always(f):
    return f()


def ifLogged(f):
    user = get_current_user(request)
    return f(user) if user is not None \
        else USER_NOT_LOGGED


def ifHasRole(f, role):
    return ifLogged(lambda user: f(user)
    if has_role(user, role)
    else USER_NOT_AUTHORIZED)


def ifAdmin(f):
    return ifHasRole(f, ADMIN)


def ifManager(f):
    return ifHasRole(f, MANAGER)


@app.route('/me', methods=['GET'])
def me():
    return ifLogged(lambda user:
                    sendResponse(parse_me(user), "", 200))


@app.route('/me', methods=['POST'])
def me_update():
    return ifLogged(lambda user:
                    doFinallyCatch(
                        lambda: update_me(user, request),
                        sendResponse({}, "Updated", 200),
                        sendResponse({}, "Error", 503)
                    ))


@app.route('/me/reservations', methods=['GET'])
def my_reservations():
    return ifLogged(lambda user:
                    sendResponse(parse_my_res(user), "", 200))


@app.route('/users', methods=['GET'])
def all_users():
    return ifAdmin(lambda user:
                   sendResponse(users_all(), "", 200))


@app.route('/slots/reservations', methods=['GET'])
def fetch_slots_reservations():
    return always(lambda:
                  sendResponse(parse_slots(), "", 200))


@app.route('/lessons/reservations', methods=['GET'])
def fetch_lessons_reservations():
    return always(lambda:
                  sendResponse(parse_lessons(), "", 200))


@app.route('/slots/add', methods=['POST'])
def add_slot_route():
    return ifManager(lambda user:
                     doFinallyCatch(
                         lambda: add_slot(request),
                         sendResponse({}, "Added", 200),
                         sendResponse({}, "Error", 503)
                     ))


@app.route('/slots/reservation', methods=['POST'])
def add_slot_reservation():
    return ifLogged(lambda user:
                    doFinallyCatch(
                        lambda: add_slot_reservation(user, request),
                        sendResponse({}, "Added", 200),
                        sendResponse({}, "Error", 503)
                    ))


@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    return always(lambda:
                  doFinallyCatch(
                      lambda: register_user(request.get_json()),
                      sendResponse({}, 'Registered successfully', 200),
                      sendResponse({}, 'Already registered', 200)
                  ))


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    return always(lambda:
                  doFinallyCatch(
                      lambda: authenticate_user(request),
                      sendResponse(authenticate_user(request),"New token", 200),
                      sendResponse({}, 'Authentication failed', 200)
                  ))


def authenticate_user(request):
    auth = request.headers
    email = auth['username']
    try_password = auth['password']
    if not auth or not email or not try_password:
        raise ValueError('Auth required.')
    user = database.get_by_email(Users, email)
    if user is None:
        raise ValueError('User does not exist.')
    if check_password_hash(user.password, try_password):
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])
        return {'token': token.decode('UTF-8')}
    raise Exception('Auth required.')

