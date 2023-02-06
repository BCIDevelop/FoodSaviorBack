from flask_restx import fields
from flask_restx.reqparse import RequestParser


class AuthRequestSchema:
    def __init__(self, namespace):
        self.namespace = namespace

    def signin(self):
        return self.namespace.model('Auth SignIn', {
            'username': fields.String(required=True),
            'password': fields.String(required=True)
        })

    def signup(self):
        return self.namespace.model('Auth SignUp', {
            'name': fields.String(required=True, min_length=2, max_length=80),
            'last_name': fields.String(required=True, min_length=2, max_length=120),
            'username': fields.String(required=True, min_length=4, max_length=80),
            'password': fields.String(required=True, min_length=4, max_length=120),
            'email': fields.String(required=True, min_length=3, max_length=140)
        })

    def refreshToken(self):
        parser = RequestParser()
        parser.add_argument(
            'Authorization', type=str, location='headers',
            help='Ej: Bearer {refresh_token}'
        )
        return parser

    def resetPassword(self):
        return self.namespace.model('Auth Reset Password', {
            'email': fields.String(required=True)
        })
