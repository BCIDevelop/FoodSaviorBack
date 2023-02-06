from flask_restx import fields
from flask_restx.reqparse import RequestParser
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow.fields import Nested
from app.models.users_model import UserModel


class UsersRequestSchema:
    def __init__(self, namespace):
        self.namespace = namespace

    def all(self):
        parser = RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        return parser

    def create(self):
        return self.namespace.model('User Create', {
            'name': fields.String(required=True, max_length=80),
            'last_name': fields.String(required=True, max_length=120),
            'username': fields.String(required=True, max_length=80),
            'password': fields.String(required=True, max_length=120),
            'email': fields.String(required=True, max_length=140),
            'rol_id': fields.Integer(required=True)
        })

    def update(self):
        return self.namespace.model('User Update', {
            'name': fields.String(required=False, max_length=80),
            'last_name': fields.String(required=False, max_length=120),
            'username': fields.String(required=False, max_length=80),
            'email': fields.String(required=False, max_length=140),
            'rol_id': fields.Integer(required=False)
        })


class UsersResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        ordered = True
        exclude = ['password']

    role = Nested('RolesResponseSchema', exclude=['users','status','id'], many=False)
