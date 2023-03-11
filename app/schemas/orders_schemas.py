from flask_restx import fields
from app.models.orders_model import OrderModel
class OrderRequestSchema:
    def __init__(self,namespace) -> None:
        self.namespace=namespace


    def create(self):
        return self.namespace.model('Order Create',{
            'coupon':fields.String(require=False,max_length=50),
            'card_token':fields.String(require=False,max_length=50),
            'plan_id':fields.Integer(required=True)
        })    