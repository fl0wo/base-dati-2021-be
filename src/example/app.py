import json

from flask import current_app, flash, jsonify, make_response, redirect, request, url_for

from . import create_app, database
from .models import Cats, Users
from .security import token_required

from werkzeug.security import generate_password_hash, \
    check_password_hash  # not constant due to salt adding (guarda rainbow table attack)
import uuid
import jwt
import datetime
from functools import wraps

app = create_app()


@app.route('/', methods=['GET'])
def fetch():
    cats = database.get_all(Cats)
    all_cats = []
    for cat in cats:
        new_cat = {
            "id": cat.id,
            "name": cat.name,
            "price": cat.price,
            "breed": cat.breed
        }

        all_cats.append(new_cat)
    return json.dumps(all_cats), 200


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

    database.add_instance(Users, id=str(uuid.uuid4()), email=data['email'], password=hashed_password)
    return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication': 'Basic realm: "login required"'})

    user = database.get_by_email(Users, auth.username)

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY']
        )
        return jsonify({'token': token.encode().decode('UTF-8')})

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
