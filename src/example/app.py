from flask import jsonify, request, make_response
from flask_cors import CORS
from . import app, UPLOAD_FOLDER, ALLOWED_EXTENSIONS

from .security import register_user, authenticate_user

from .response import Response

from .controllers.user_controller import \
    parse_me, update_me, parse_my_res, users_all, courses_all, users_trainers_all, current_policy, accesses_all

from .controllers.slot_controller import \
    parse_slots, slot_add_reservation, add_slot, add_lesson, add_course, lesson_add_reservation

from .controllers.lesson_controller import \
    parse_lessons

from .utils.domainutils import doFinallyCatch, \
    always, ifLogged, ifAdmin, ifManager, ifTrainer

from .utils.fileuploaderutils import upload_file, download_profilepic

from flask_restx import Api, Resource, fields, Namespace

from .utils.swaggerutils import api, user_api, token_api, \
    update_user_api, mess_of_string,mess_of, mess_ofs, me_ns, users_ns, slot_ns, \
    lesson_ns


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
    return r
    #return make_response(jsonify(r.toJSON()), 200, basicHeaders)

def sendResponseJson(payload, msg, status):
    r = sendResponse(payload, msg, status)
    return make_response(jsonify(r.toJSON()), 200, basicHeaders)


@me_ns.route('')
@me_ns.param('x-access-token', 'A valid JWT token')
class Me(Resource):

    @me_ns.marshal_with(mess_of(user_api))
    def get(self):
        return ifLogged(lambda user:
                        sendResponse(parse_me(user), "", 200))

    @me_ns.expect(update_user_api)
    @me_ns.marshal_with(mess_of_string())
    def post(self):
        return ifLogged(lambda user:
                        doFinallyCatch(
                            lambda: update_me(user, request),
                            sendResponse({}, "Updated", 200),
                            sendResponse({}, "Error", 400)
                        ))


@users_ns.route('/trainers/all')
class Trainers(Resource):
    @api.marshal_with(mess_ofs(user_api))
    def get(self):
        return ifTrainer(lambda user:
                         sendResponse(users_trainers_all(), "", 200))

@users_ns.route('/all', methods=['GET'])
class Users(Resource):
    def get(self):
        return ifAdmin(lambda user:
                       sendResponseJson(users_all(), "", 200))


@me_ns.route('/profilepic')
class Picture(Resource):
    def get(self):
        return ifLogged(lambda user:
                        download_profilepic(user.id))

    @api.marshal_with(mess_of_string())
    def post(self):
        return ifLogged(lambda user:
                        doFinallyCatch(
                            lambda: upload_file(user.id),
                            sendResponse({}, "Uploaded", 200),
                            sendResponse({}, "Error", 400)
                        ))


@me_ns.route('/reservations', methods=['GET'])
class Reservations(Resource):
    def get(self):
        return ifLogged(lambda user:
                        sendResponseJson(parse_my_res(user), "", 200))


@slot_ns.route('')
class Slots(Resource):
    def get(self):
        return always(lambda: sendResponseJson(parse_slots(), "", 200))

    def post(self):
        return ifManager(lambda user:
                         doFinallyCatch(
                             lambda: add_slot(request),
                             sendResponseJson({}, "Added", 200),
                             sendResponseJson({}, "Error", 503)
                         ))


@slot_ns.route('/reservation')
class SlotReservations(Resource):
    def post(self):
        return ifLogged(lambda user:
                        doFinallyCatch(
                            lambda: slot_add_reservation(user, request),
                            sendResponseJson({}, "Added", 200),
                            sendResponseJson({}, "Error", 503)
                        ))


@lesson_ns.route('/add')
class LessonAdd(Resource):
    def post(self):
        return ifTrainer(lambda user:
                         doFinallyCatch(
                             lambda: add_lesson(request),
                             sendResponseJson({}, "Added", 200),
                             sendResponseJson({}, "Error", 503)
                         ))

@lesson_ns.route('/reservation')
class LessonsReservation(Resource):
    def get(self):
        return always(lambda:
                      sendResponseJson(parse_lessons(), "", 200))

    def post(self):
        return ifLogged(lambda user:
                        doFinallyCatch(
                            lambda: lesson_add_reservation(user, request),
                            sendResponseJson({}, "Added", 200),
                            sendResponseJson({}, "Error", 503)
                        ))


@api.route('/courses')
class Courses(Resource):
    def get(self):
        return always(lambda:
                         sendResponseJson(courses_all(), "", 200))

    def post(self):
        return ifTrainer(lambda user:
                         doFinallyCatch(
                             lambda: add_course(request),
                             sendResponseJson({}, "Added", 200),
                             sendResponseJson({}, "Error", 503)
                         ))


@api.route('/policies')
class Policies(Resource):
    def get(self):
        return always(lambda:
                         sendResponseJson(current_policy(), "", 200))

@api.route('/accesses')
class Accesses(Resource):
    def get(self):
        return ifLogged(lambda user:
                        sendResponseJson(accesses_all(user), "", 200))


@api.route('/register', methods=['GET', 'POST'])
class Register(Resource):
    def post(self):
        return always(lambda:
                      doFinallyCatch(
                          lambda: register_user(request.get_json()),
                          sendResponseJson({}, 'Registered successfully', 200),
                          sendResponseJson({}, 'Already registered', 400)
                      ))


@api.route('/login', methods=['GET', 'POST'])
class Login(Resource):
    @api.marshal_with(mess_of(token_api))
    def get(self):
        return always(lambda:
                      doFinallyCatch(
                          lambda: authenticate_user(request),
                          sendResponse(authenticate_user(request), "New token", 200),
                          sendResponse({}, 'Authentication failed', 400)
                      ))
