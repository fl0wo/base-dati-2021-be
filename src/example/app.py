from flask import jsonify, request,make_response
from flask_cors import CORS
from . import app, UPLOAD_FOLDER, ALLOWED_EXTENSIONS

from .security import register_user, authenticate_user

from .response import Response

from .controllers.user_controller import \
    parse_me, update_me, parse_my_res, users_all, courses_all, users_trainers_all

from .controllers.slot_controller import \
    parse_slots, slot_add_reservation, add_slot, add_lesson, add_course

from .controllers.lesson_controller import \
    parse_lessons

from .utils.domainutils import doFinallyCatch, \
    always, ifLogged, ifAdmin, ifManager, ifTrainer

from .utils.fileuploaderutils import upload_file, download_profilepic

from flask_restx import Api, Resource, fields

CORS(app)

basicHeaders = [
    ('Content-Type', 'application/json'),
    ('Access-Control-Allow-Origin', '*'),
    ('Access-Control-Allow-Headers', 'Authorization, Content-Type'),
    ('Access-Control-Allow-Methods', 'POST'),
]

api = Api(app, version='1.0',
          title='Gym API',
          description='Gym BackEnd Api',
          )

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})


def sendResponse(payload, msg, status):
    r = Response()
    r.data = payload
    r.message = msg
    r.status = status
    return make_response(jsonify(r.toJSON()), 200,basicHeaders)


@api.route('/me')
@api.param('x-access-token', 'A valid JWT token')
class Me(Resource):
    @api.doc(id='getMe')
    @api.response(200, 'Success', headers={'X-Header': 'Some header'})
    def get(self):
        return ifLogged(lambda user:
                        sendResponse(parse_me(user), "", 200))

    @api.doc(id='updateMe')
    def post(self):
        return ifLogged(lambda user:
                        doFinallyCatch(
                            lambda: update_me(user, request),
                            sendResponse({}, "Updated", 200),
                            sendResponse({}, "Error", 400)
                        ))


@api.route('/me/profilepic')
@api.doc(id='getMyProfilePic')
class Picture(Resource):
    def get(self):
        return ifLogged(lambda user:
                        download_profilepic(user.id))

    def post(self):
        return ifLogged(lambda user:
                        doFinallyCatch(
                            lambda: upload_file(user.id),
                            sendResponse({}, "Uploaded", 200),
                            sendResponse({}, "Error", 400)
                        ))


@app.route('/me/reservations', methods=['GET'])
def my_reservations():
    return ifLogged(lambda user:
                    sendResponse(parse_my_res(user), "", 200))


@app.route('/users', methods=['GET'])
def all_users():
    return ifAdmin(lambda user:
                   sendResponse(users_all(), "", 200))


@app.route('/users/trainers/all', methods=['GET'])
def all_trainers():
    return ifTrainer(lambda user:
                     sendResponse(users_trainers_all(), "", 200))


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


@app.route('/lessons/add', methods=['POST'])
def add_lesson_route():
    return ifTrainer(lambda user:
                     doFinallyCatch(
                         lambda: add_lesson(request),
                         sendResponse({}, "Added", 200),
                         sendResponse({}, "Error", 503)
                     ))


@app.route('/courses/add', methods=['POST'])
def add_course_route():
    return ifTrainer(lambda user:
                     doFinallyCatch(
                         lambda: add_course(request),
                         sendResponse({}, "Added", 200),
                         sendResponse({}, "Error", 503)
                     ))


@app.route('/slots/reservation', methods=['POST'])
def add_slot_reservation():
    return ifLogged(lambda user:
                    doFinallyCatch(
                        lambda: slot_add_reservation(user, request),
                        sendResponse({}, "Added", 200),
                        sendResponse({}, "Error", 503)
                    ))


@app.route('/courses/all', methods=['GET'])
def fetch_all_courses():
    return ifTrainer(lambda user:
                     sendResponse(courses_all(), "", 200))


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
