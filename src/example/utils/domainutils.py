from ..security import get_current_user, has_role, ADMIN, MANAGER, TRAINER
from flask import jsonify,request

USER_NOT_LOGGED = jsonify({'message': 'user not logged'}), 401
USER_NOT_AUTHORIZED = jsonify({'message': 'user not authorized'}), 401

def doFinallyCatch(do, success, catch):
    try:
        res = do()
        if res is not None and res is False:
            return catch
    except Exception as e:
        print(e) #Molto buono per debug
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
    return ifHasRole(f, MANAGER) or ifAdmin(f)

def ifTrainer(f):
    return ifHasRole(f, TRAINER) or ifAdmin(f)
