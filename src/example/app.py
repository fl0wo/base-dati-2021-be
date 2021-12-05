from flask import jsonify, request
from flask_cors import CORS
from . import app , UPLOAD_FOLDER, ALLOWED_EXTENSIONS

from .security import register_user, authenticate_user

from .response import Response

from .controllers.user_controller import \
    parse_me, update_me, parse_my_res, users_all

from .controllers.slot_controller import \
    parse_slots, add_slot_reservation, add_slot

from .controllers.lesson_controller import \
    parse_lessons

from .utils.domainutils import doFinallyCatch, \
    always, ifLogged, ifAdmin, ifManager

from .utils.fileuploaderutils import upload_file, download_profilepic

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
    return jsonify(r.toJSON()), 200, basicHeaders


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
                        sendResponse({}, "Error", 400)
                    ))

@app.route('/me/profilepic', methods=['POST'])
def me_profilepic():
    return ifLogged(lambda user:
                    doFinallyCatch(
                        lambda: upload_file(user.id),
                        sendResponse({}, "Uploaded", 200),
                        sendResponse({}, "Error", 400)
                    ))

@app.route('/me/profilepic',methods=['GET'])
def download_file():
    return ifLogged(lambda user:
                    download_profilepic(user.id))

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
    return always(lambda: sendResponse(parse_slots(), "", 200))


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
                      sendResponse({}, 'Already registered', 400)
                  ))


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    return always(lambda:
                  doFinallyCatch(
                      lambda: authenticate_user(request),
                      sendResponse(authenticate_user(request), "New token", 200),
                      sendResponse({}, 'Authentication failed', 400)
                  ))
