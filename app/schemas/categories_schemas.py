from flask_restx import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.categories_model import CategoryModel
from flask_restx.reqparse import RequestParser

class CategoriesRequestSchema:
    def __init__(self,namespace) -> None:
        self.namespace=namespace

    def all(self):
        parser = RequestParser()
        parser.add_argument('page',type=int,default=1,location='args')
        parser.add_argument('per_page',type=int,default=5,location='args')
        return parser

    def create(self):
        return self.namespace.model('Categoriy create',{
            'name': fields.String(required=True,max_length=120)
        })
    def update(self):
        return self.namespace.model('Categoriy update',{
            "name": fields.String(required=True,max_length=120)
        })     

 

class CategoriyResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model=CategoryModel
        ordered=True
    
