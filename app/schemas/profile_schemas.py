from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.users_model import UserModel
from flask_restx.reqparse import RequestParser
from werkzeug.datastructures import FileStorage
class ProfileRequestSchema:
    def __init__(self,namespace) -> None:
        self.namespace=namespace

    def update(self):
        parser=RequestParser()
        
        parser.add_argument('avatar',type=FileStorage,required=False,location='files')
        parser.add_argument('username',type=str,required=False,location='form')
        parser.add_argument('last_name',type=str,required=False,location='form')
        parser.add_argument('name',type=str,required=False,location='form')
        parser.add_argument('password',type=str,required=False,location="form")
        parser.add_argument('new_password',type=str,required=False,location="form")

        return parser
   

class ProfileResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model=UserModel
        ordered=True
        exclude = ['password']