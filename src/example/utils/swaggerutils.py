from .. import app
from flask_restx import Api, Resource, fields, Namespace

api = Api(app, version='1.0',
          title='Gym API',
          description='Gym BackEnd Api')

me_ns = Namespace('me', description='Operations related to the currently logged user.')
users_ns = Namespace('users', description='Operations related to all users [admin,trainer required].')
slot_ns = Namespace('slots', description='Operations related to slots [manager required].')
lesson_ns = Namespace('lessons', description='Operations related to lessons [trainer required].')

api.add_namespace(me_ns)
api.add_namespace(users_ns)
api.add_namespace(slot_ns)
api.add_namespace(lesson_ns)

user_api = api.model('User', {
    'name': fields.String(readonly=True, description='The user first name'),
    'surname': fields.String(required=True, description='The user last name'),
    'role': fields.String(required=True, description='The role assigned to user'),
    'email': fields.String(required=True, description='The user email'),
    'birth_date': fields.Date(required=True, description='The date user born'),
    'fiscal_code': fields.String(required=True, description='The user fiscal id'),
    'id': fields.String(readonly=True, description='The user id')
})

update_user_api = api.model('UpdateUser', {
    'phone': fields.String(required=False, description='The user phone'),
    'birth_date': fields.Date(required=False, description='The date user born'),
    'fiscal_code': fields.String(required=False, description='The user fiscal id')
})

token_api = api.model('Token',{
    'token': fields.String(required=True, description='Valid JWT token returned by be.')
})

def mess_of_string():
    return api.model('MessageResponse', {
        'status': fields.String(required=True, description='The HTTP code status'),
        'message': fields.String(required=True, description='A message sent from be'),
        'data': fields.String(required=True, description='Message')
    })

def mess_of(model):
    return api.model('MessageResponse', {
        'status': fields.String(required=True, description='The HTTP code status'),
        'message': fields.String(required=True, description='A message sent from be'),
        'data': fields.Nested(model)
    })

def mess_ofs(model):
    return api.model('MessageResponse', {
        'status': fields.String(required=True, description='The HTTP code status'),
        'message': fields.String(required=True, description='A message sent from be'),
        'data': fields.List(fields.Nested(model))
    })