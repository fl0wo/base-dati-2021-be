from werkzeug.security import generate_password_hash, \
    check_password_hash  # not constant due to salt adding (guarda rainbow table attack)
import uuid
import jwt
import datetime
from functools import wraps

from .app import *
from .database import get_by_id
from .models import Users


# si prende f e la decora concatenando new checktoken fun
def token_required(f):
    @wraps(f)
    def dec(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'token is missing'})

        try:
            data = jwt.decode(token, app.config[SECRET_KEY])
            current_user = get_user_by_id(Users, data['id'])
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return dec
