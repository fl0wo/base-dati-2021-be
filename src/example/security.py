from werkzeug.security import generate_password_hash, \
    check_password_hash  # not constant due to salt adding (guarda rainbow table attack)
import uuid
import jwt
import datetime
from functools import wraps

from . import config, database, app
from .database import get_by_id
from .models import Users

ADMIN = "admin"
MANAGER = "manager"
TRAINER = "trainer"
CUSTOMER = "customer"


def rolelvl(role):
    if role == ADMIN:
        return 4
    if role == MANAGER:
        return 3
    if role == TRAINER:
        return 2
    if role == CUSTOMER:
        return 1
    return 0


def get_current_user(request):
    try:
        token = get_token(request.headers)
        data = jwt.decode(token, config.secret)
        return get_by_id(Users, data['id'])
    except:
        return None


def is_logged(request):
    user = get_current_user(request)
    return user is not None


def has_role(user, desired_role):
    if user is None:
        return None
    if rolelvl(user.role) < rolelvl(desired_role):
        return False
    return True


def get_current_manager(request):
    user = get_current_user(request)
    return has_role(user, MANAGER)


def get_token(headers):
    return headers['x-access-token']


def get_decorator():
    def decorator(func):

        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                return jsonify({'message': error.args[0]}), 401

        return new_func

    return decorator


require_token = get_decorator()


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


def register_user(data):
    hashed_password = generate_password_hash(data['password'], method='sha256')
    database.add_instance(Users,
                          id=str(uuid.uuid4()),
                          email=data['email'],
                          password=hashed_password,
                          name=data['name'],
                          surname=data['surname'],
                          role=CUSTOMER)


def authenticate_user(request):
    auth = request.headers
    email = auth['username']
    try_password = auth['password']
    if not auth or not email or not try_password:
        return False
    user = database.get_by_email(Users, email)
    if user is None:
        return False
    if check_password_hash(user.password, try_password):
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])
        return {'token': token.decode('UTF-8')}
    return False
