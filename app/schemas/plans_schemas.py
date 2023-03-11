from flask_restx.reqparse import RequestParser
from flask_restx import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.plans_model import PlanModel
class PlanRequestSchema :
    def __init__(self,namespace) -> None:
        self.namespace=namespace


    def all(self):
        parser=RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        return parser
    
    def create(self):
        return self.namespace.model('Plans Create',{
            'name':fields.String(max_length=20,required=True),
            'price':fields.Float(precision=2,required=True),
        })

    def update(self):
        return self.namespace.model('Plans Update',{
            'name':fields.String(max_length=20,required=False),
            'price':fields.Float(precision=2,required=False),
        }) 

class PlanResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        ordered=True
        model=PlanModel