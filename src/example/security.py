from werkzeug.security import generate_password_hash, \
    check_password_hash  # not constant due to salt adding (guarda rainbow table attack)
import uuid
import jwt
import datetime
from functools import wraps

from . import config
from .database import get_by_id
from .models import Users

ADMIN = "admin"
MANAGER = "manager"
TRAINER = "trainer"
CUSTOMER = "customer"


def rolelvl(role):
    if role == ADMIN:
        return 4
    if role == 'manager':
        return 3
    if role == 'trainer':
        return 2
    if role == 'customer':
        return 1
    return 0


def get_current_user(request):
    token = get_token(request.headers)
    data = jwt.decode(token, config.secret)
    return get_by_id(Users, data['id'])


def check_user_role(user, desired_role):
    if rolelvl(user.role) < rolelvl(desired_role):
        return jsonify({'message': "insufficient role"}), 401
    return user


def get_current_admin(request):
    user = get_current_user(request)
    return check_user_role(user, ADMIN)


def get_current_manager(request):
    user = get_current_user(request)
    return check_user_role(user, MANAGER)


def get_token(headers):
    return headers['x-access-token']


def require_token(func):
    @wraps(func)
    def func_with_handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (BadTokenError, MissingTokenError) as error:
            return jsonify({'message': error.args[0]}), 401

    return func_with_handler


def role_required(func, min_desired_role):
    @wraps(func)
    def f(*args, **kwargs):
        try:
            user = args
            if user.role != min_desired_role:
                return jsonify({'message': "not authorized"}), 401
        except (BadTokenError, MissingTokenError) as error:
            return jsonify({'message': error.args[0]}), 401

    return f


def admin_required(func):
    return role_required(func, "admin")


def manager_required(func):
    return role_required(func, "manager")
