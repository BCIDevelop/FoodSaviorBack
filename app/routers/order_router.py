from app import api
from flask_restx import Resource
from app.schemas.orders_schemas import OrderRequestSchema
from app.controllers.order_controller import OrderController
from flask_jwt_extended import jwt_required

order_ns=api.namespace(
    name='Ordenes de compra',
    description ='Rutas para el modelo Ordenes',
    path='/orders'
)
request_schema=OrderRequestSchema(order_ns)
@order_ns.route('')
@order_ns.doc(security='Bearer')
class Order(Resource):
    @jwt_required()
    @order_ns.expect(request_schema.create(),validate=True)
    def post(self):
        """ Creacion de un pedido """
        controller=OrderController()
       
        return controller.create(order_ns.payload)
        

