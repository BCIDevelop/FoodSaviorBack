from flask_restx import fields
from flask_restx.reqparse import RequestParser
class MercadoPagoRequestSchema():
    def __init__(self,namespace) -> None:
        
        self.namespace=namespace

    def createUserTest(self):
        return self.namespace.model('Mercado Pago User Test Create',{
            'description':fields.String(required=True)
        })    
    def createPlan(self):
        return self.namespace.model('Mercado Pago Create Plan',{
            'plan_id':fields.Integer(required=True)
        })    
    def updatePlan(self):
        return self.namespace.model('Mercado Pago Create Plan',{
            'mercadopago_plan_id':fields.String(required=True),
            'code':fields.String(required=True)
        })   
    def listPlan(self):
        parser=RequestParser()
        parser.add_argument('mercadopago_plan_id', type=str, location='args')
        
        return parser  