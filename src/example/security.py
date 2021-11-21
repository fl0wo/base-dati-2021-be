from werkzeug.security import generate_password_hash, \
    check_password_hash  # not constant due to salt adding (guarda rainbow table attack)
import uuid
import jwt
import datetime
from functools import wraps

from . import config
from .database import get_by_id
from .models import Users


def get_current_user(request):
    token = get_token(request.headers)
    data = jwt.decode(token, config.secret)
    return get_by_id(Users, data['id'])


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


def admin_required(func):
    @wraps(func)
    def f(*args, **kwargs):
        try:
            user = args
            if user.role != "admin":
                return jsonify({'message': "not authorized"}), 401
        except (BadTokenError, MissingTokenError) as error:
            return jsonify({'message': error.args[0]}), 401
    return f


