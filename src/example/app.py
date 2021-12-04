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
    ADMIN, MANAGER, CUSTOMER, TRAINER

from .response import Response, DATE_FORMAT, \
    DATE_FORMAT_IN, TIME_FORMAT

from werkzeug.security import generate_password_hash, \
    check_password_hash  # not constant due to salt adding (guarda rainbow table attack)

from .controllers.user_controller import \
    parse_me, update_me, parse_my_res, users_all

from .controllers.slot_controller import \
    parse_slots

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
    except:
        return catch
    finally:
        return success


def always(f):
    return f()


def ifLogged(f):
    user = get_current_user(request)
    if user is None:
        return USER_NOT_LOGGED
    return f(user)


def ifAdmin(f):
    return ifLogged(lambda user: f(user)
    if has_role(user, ADMIN)
    else USER_NOT_AUTHORIZED)


@app.route('/me', methods=['GET'])
def me():
    return ifLogged(lambda user:
                    sendResponse(parse_me(user), "", 200))


@app.route('/me', methods=['POST'])
def me_update():
    return ifLogged(lambda user:
                    doFinallyCatch(
                        update_me(user, request),
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
def addSlot():
    manager = get_current_manager(request)
    if manager is None:
        return jsonify({'message': 'user not logged'}), 401
    if manager is False:
        return jsonify({'message': 'role not sufficient'}), 401

    body = request.get_json()
    # TODO: check that timefrom < timeto
    database.add_instance(Slots,
                          id=str(uuid.uuid4()),
                          date=body['date'],
                          time_from=body['time_from'],
                          time_to=body['time_to'],
                          max_capacity=body['max_capacity'],  # TODO: check if > 1
                          title=body['title'],
                          description=body['description'],
                          )

    return sendResponse({}, "Added", 200)


@app.route('/slots/reservation', methods=['POST'])
def addSlotReservation():
    user = get_current_user(request)
    if user is None:
        return jsonify({'message': 'user not logged'}), 401

    body = request.get_json()

    # database.begin_transaction() ---> sqlalchemy.exc.InvalidRequestError: A transaction is already begun on this Session.
    # TODO Cercare di capire come evitare sql injections, o facciamo dei controlli sul parametro oppure bisogna cambiare modo di fare le query
    db_is_space = database.check_if_space_for_slot_reservation(user.id)
    is_space = db_is_space[0]['there_is_space']  # TODO IVAN Controlla se sta roba funziona
    if is_space == 0:
        return sendResponse({}, "Not enough space in slot", 401)

    reservation_id = str(uuid.uuid4())
    database.add_instance_no_commit(Reservations,
                                    id=reservation_id,
                                    customer=body['idUser'],
                                    room='1')
    database.add_instance_no_commit(WeightRoomReservations,
                                    reservation_number=999,
                                    # FIXME TODO: MANDARGLI DA FRONT END/ fare query qui x prendersi il progressivo della reservation x quel determinato slot oppure eliminare il campo perche non viene mai usato
                                    reservation_id=reservation_id,
                                    slot=(body['idSlot']))
    database.commit_changes()

    return sendResponse({}, "Subscribed to slot", 200)


@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    try:
        database.add_instance(Users,
                              id=str(uuid.uuid4()),
                              email=data['email'],
                              password=hashed_password,
                              name=data['name'],
                              surname=data['surname'])
    except:
        return sendResponse({}, 'already registered', 200)

    return sendResponse({}, 'registered successfully', 200)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.headers

    email = auth['username']
    try_password = auth['password']
    if not auth or not email or not try_password:
        return sendResponse({'Authentication': 'Basic realm: "login required"'}, 'could not verify', 401)

    user = database.get_by_email(Users, email)

    if check_password_hash(user.password, try_password):
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY']
        )
        return sendResponse({'token': token.decode('UTF-8')}, "New token", 200)

    return sendResponse({'WWW.Authentication': 'Basic realm: "login required"'}, 'could not verify', 401)

# @app.route('/remove/<cat_id>', methods=['DELETE'])
# def remove(cat_id):
#     database.delete_instance(Cats, id=cat_id)
#     r = Response
#     r.message = json.dumps("Deleted")
#     return jsonify(r);


# @app.route('/edit/<cat_id>', methods=['PATCH'])
# def edit(cat_id):
#     data = request.get_json()
#     new_price = data['price']
#     database.edit_instance(Cats, id=cat_id, price=new_price)
#     r = Response
#     r.message = json.dumps("Edited")
#     return jsonify(r);
