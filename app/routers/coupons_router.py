from app import api
from flask_restx import Resource
from app.schemas.coupons_schemas import CouponRequestSchema
from app.controllers.coupons_controller import CouponController
from flask_jwt_extended import jwt_required
coupon_ns=api.namespace(
    name='Cupones',
    description='Rutas del modelo de cupones',
    path='/coupons'
)
request_parser=CouponRequestSchema(coupon_ns)
@coupon_ns.route('')
@coupon_ns.doc(security='Bearer')
class coupons(Resource):
    @coupon_ns.expect(request_parser.all())
    @jwt_required()
    def get(self):
        """ Listar todos los cuponess """
        controller=CouponController()
        query=request_parser.all().parse_args()
        return controller.all(query)

    @coupon_ns.expect(request_parser.create(),validate=True)
    @jwt_required()
    def post(self):
        """ Crear un cupones """
        controller=CouponController()
        return controller.create(coupon_ns.payload)


@coupon_ns.route('/<int:id>')
@coupon_ns.doc(security='Bearer')
class CouponById(Resource):
    @jwt_required()
    def get(self,id):
        """ Obtener cupones por ID """
        controller=CouponController()
        return controller.getById(id)

    @coupon_ns.expect(request_parser.update(),validate=True)
    @jwt_required()
    def patch(self,id):
        """ Actualizar cupones por ID """
        controller=CouponController()
        return controller.update(id,coupon_ns.payload)
    @jwt_required()
    def delete(self,id):
        """ Deshabilitar un cupones por ID"""
        controller=CouponController()
        return controller.delete(id)

    @coupon_ns.route('/validate/<code>')
    @coupon_ns.doc(security='Bearer')
    class CouponByCode(Resource):
        @jwt_required()
        def get(self,code):
            """ Validar cupones por codigo """
            controller=CouponController()
            return controller.validate(code)
    