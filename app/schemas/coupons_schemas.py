from flask_restx import fields
from flask_restx.reqparse import RequestParser
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.coupons_model import CouponModel

class CouponRequestSchema:
    def __init__(self,namespace) -> None:
        self.namespace=namespace

    def all(self):
        parser=RequestParser()
        parser.add_argument('page',type=int,default=1,location='args')
        parser.add_argument('per_page',type=int,default=5,location='args')
        return parser    

    def create(self):
        return self.namespace.model('Coupon Create',{
             'code':fields.String(required=True,max_length=50),
             'percentage':fields.Float(required=True,precision=2),
            'started_at':fields.DateTime(required=True),
            'ended_at':fields.DateTime(required=True),

        })
    
    def update(self):
        return self.namespace.model('Coupon Update',{
            'code':fields.String(required=False,max_length=50),
             'percentage':fields.Float(required=False,precision=2),
            'started_at':fields.DateTime(required=False),
            'ended_at':fields.DateTime(required=False),
            
        })


class CouponsResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model=CouponModel
        ordered=True    
