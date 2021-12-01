import json

from flask import current_app, flash, jsonify, make_response, redirect, request, url_for
from flask_cors import CORS
from . import create_app, database
from .models import Cats, Users, Slots
from .security import admin_required, require_token, get_current_user
from .response import Response
from werkzeug.security import generate_password_hash, \
    check_password_hash  # not constant due to salt adding (guarda rainbow table attack)
import uuid
import jwt
import datetime
from functools import wraps

DATE_FORMAT = '%Y/%m/%d'

TIME_FORMAT = "%H:%M:%S"

app = create_app()
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


@require_token
@app.route('/me', methods=['GET'])
def me():
    user = get_current_user(request)

    data = {
        "name": user.name,
        "surname": user.surname,
        "role": user.role,
        "email": user.email
    }
    return sendResponse(data, "", 200)


@app.route('/users', methods=['GET'])
def fetch():
    dbusers = database.get_all(Users)
    users = []
    for user in dbusers:
        users.append({
            "name": user.name,
            "surname": user.surname,
            "role": user.role,
            "email": user.email
        })
    return sendResponse(json.dumps(users), "", 200)


@app.route('/slotsReservations', methods=['GET'])
def fetchSlotsReservations():
    dbSlots = database.get_all_slots_curent_reservation()
    slots = []
    for s in dbSlots:
        slots.append({
            "id": s['id'],
            "date": (s['date']).strftime(DATE_FORMAT),
            "time_from": s['time_from'].strftime(TIME_FORMAT),
            "time_to": s['time_to'].strftime(TIME_FORMAT),
            "max_capacity": s['max_capacity'],
            "current_reservations": s['current_reservations']
        })
    return sendResponse(slots, "", 200)


@app.route('/slots/add', methods=['POST'])
def addSlot():
    body = request.get_json()

    database.add_instance(Slots,
                          id=str(uuid.uuid4()),
                          date=body.date,
                          time_from=body.time_from,
                          time_to=body.time_to,
                          max_capacity=body.max_capacity,  # TODO: check if > 1
                          title=body.title,
                          description=body.description,
                          )

    return sendResponse({}, "Added", 200)


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
        r.data = jsonify({'token': token.decode('UTF-8')})
        return jsonify(r)

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
