from app import api
from flask_restx import Resource
from app.schemas.mercadopago_schemas import MercadoPagoRequestSchema
from app.utils.mercadopago import MercadoPago
from flask import request
from app.controllers.mercadopago_controller import MercadoPagoController

mercadopago_ns=api.namespace(
    name='Mercado Pago',
    description ='Rutas para la integracion con Mercado Pago',
    path='/mercadopago'
)
request_schema=MercadoPagoRequestSchema(mercadopago_ns)
@mercadopago_ns.route('/users/test')
class UserTest(Resource):
    @mercadopago_ns.expect(request_schema.createUserTest(),validate=True)
    def post(self):
        """ Crear usuario de prueba """
        mercadopago=MercadoPago()
        return mercadopago.createUserTest(mercadopago_ns.payload)

@mercadopago_ns.route('/webhook')
class Webhook(Resource):
    def post(self):
        """ Recepcion notificacion de pagos """
        query=request.args.to_dict()
        payment_id=query['data.id']
        controller=MercadoPagoController()
        controller.updatePaymentStatus(payment_id)
        return {},200
    
@mercadopago_ns.route('/plan')
class Plan(Resource):
    @mercadopago_ns.expect(request_schema.createPlan(),validate=True)
    def post(self):
        """ Crear plan """
        controller=MercadoPagoController()
        return controller.createPlan(mercadopago_ns.payload)    
    @mercadopago_ns.expect(request_schema.updatePlan(),validate=True)
    def put(self):
        """ Actualizar plan """
        controller=MercadoPagoController()
        return controller.updatePlan(mercadopago_ns.payload)    
    @mercadopago_ns.expect(request_schema.listPlan(),validate=True)
    def get(self):
        """ listar plan"""
        query = request_schema.listPlan().parse_args()
        controller=MercadoPagoController()
        return controller.listPlans(query)    