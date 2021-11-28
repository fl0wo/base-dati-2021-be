import json

from flask import current_app, flash, jsonify, make_response, redirect, request, url_for
from flask_cors import CORS


from . import create_app, database
from .models import Cats, Users
from .security import admin_required, require_token, get_current_user

from werkzeug.security import generate_password_hash, \
    check_password_hash  # not constant due to salt adding (guarda rainbow table attack)
import uuid
import jwt
import datetime
from functools import wraps

app = create_app()
CORS(app)


@require_token
@app.route('/me', methods=['GET'])
def me():
    user = get_current_user(request)
    return jsonify({
        "name": user.name,
        "surname": user.surname,
        "role": user.role,
        "email": user.email
    }), 200


@app.route('/users', methods=['GET'])
def fetch():
    dbusers = database.get_all(Users)
    users = []
    for user in dbusers:
        users.append({
            "name": user.name,
            "surname": user.surname,
            "role": user.role,
            "email" : user.email
        })
    return json.dumps(users), 200


@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    name = data['name']
    price = data['price']
    breed = data['breed']

    database.add_instance(Cats, name=name, price=price, breed=breed)
    return json.dumps("Added"), 200


@app.route('/remove/<cat_id>', methods=['DELETE'])
def remove(cat_id):
    database.delete_instance(Cats, id=cat_id)
    return json.dumps("Deleted"), 200


@app.route('/edit/<cat_id>', methods=['PATCH'])
def edit(cat_id):
    data = request.get_json()
    new_price = data['price']
    database.edit_instance(Cats, id=cat_id, price=new_price)
    return json.dumps("Edited"), 200


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
        return jsonify({'message': 'already registered'})

    return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.headers

    email = auth['username']
    try_password = auth['password']

    if not auth or not email or not try_password:
        return make_response('could not verify', 401, {'Authentication': 'Basic realm: "login required"'})

    user = database.get_by_email(Users, email)

    if check_password_hash(user.password, try_password):
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY']
        )
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
