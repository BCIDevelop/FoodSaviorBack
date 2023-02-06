from app import api
from flask_restx import Resource
from flask import request
from app.controllers.users_controller import UserController
from app.schemas.users_schemas import UsersRequestSchema
from flask_jwt_extended import jwt_required
from app.helpers.decorators import role_required

user_ns = api.namespace(
    name='Usuarios',
    description='Rutas del modulo Usuarios',
    path='/users'
)

request_schema = UsersRequestSchema(user_ns)


@user_ns.route('')
@user_ns.doc(security='Bearer')
class Users(Resource):
    @jwt_required()
    @user_ns.expect(request_schema.all())
    def get(self):
        ''' Listar todos los usuarios '''
        query = request_schema.all().parse_args()
        controller = UserController()
        return controller.all(query)

    @jwt_required()
    @role_required(rol_id=1)
    @user_ns.expect(request_schema.create(), validate=True)
    def post(self):
        ''' Creación de Usuario '''
        controller = UserController()
        return controller.create(request.json)


@user_ns.route('/<int:id>')
@user_ns.doc(security='Bearer')
class UserById(Resource):
    @jwt_required()
    def get(self, id):
        ''' Obtener un usuario por el ID '''
        controller = UserController()
        return controller.getById(id)

    @jwt_required()
    @role_required(rol_id=1)
    @user_ns.expect(request_schema.update(), validate=True)
    def put(self, id):
        ''' Actualizar un usuario por el ID '''
        controller = UserController()
        return controller.update(id, request.json)

    @jwt_required()
    @role_required(rol_id=1)
    def delete(self, id):
        ''' Inhabilitar un usuario por el ID '''
        controller = UserController()
        return controller.delete(id)


@user_ns.route('/profile/me')
@user_ns.doc(security='Bearer')
class UserByProfile(Resource):
    @jwt_required()
    def get(self):
        ''' Obtener los datos del usuario conectado '''
        controller = UserController()
        return controller.profileMe()
