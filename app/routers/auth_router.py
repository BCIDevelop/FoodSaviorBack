from app import api
from flask_restx import Resource
from flask import request
from app.schemas.auth_schemas import AuthRequestSchema
from app.controllers.auth_controller import AuthController
from flask_jwt_extended import jwt_required, get_jwt_identity


auth_ns = api.namespace(
    name='Autenticación',
    description='Rutas del modulo Autenticación',
    path='/auth'
)

request_schema = AuthRequestSchema(auth_ns)


@auth_ns.route('/signin')
class SignIn(Resource):
    @auth_ns.expect(request_schema.signin(), validate=True)
    def post(self):
        ''' Login de usuario '''
        controller = AuthController()
        return controller.signIn(request.json)


@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(request_schema.signup(), validate=True)
    def post(self):
        ''' Registro de usuario '''
        controller = AuthController()
        return controller.signUp(request.json)


@auth_ns.route('/token/refresh')
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    @auth_ns.expect(request_schema.refreshToken())
    def post(self):
        ''' Obtener un nuevo access token del refresh token '''
        identity = get_jwt_identity()
        controller = AuthController()
        return controller.refreshToken(identity)


@auth_ns.route('/reset_password')
class ResetPassword(Resource):
    @auth_ns.expect(request_schema.resetPassword(), validate=True)
    def post(self):
        ''' Resetear la contraseña del correo '''
        controller = AuthController()
        return controller.resetPassword(request.json)
