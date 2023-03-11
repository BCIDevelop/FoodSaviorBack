from app import api
from flask import request
from flask_restx import Resource
from app.controllers.plans_controller import PlanController
from app.schemas.plans_schemas import PlanRequestSchema
from flask_jwt_extended import jwt_required

plan_ns = api.namespace(
    name='Plans',
    description='Rutas del modelo de Plans',
    path='/plans'
)

request_schema = PlanRequestSchema(plan_ns)


@plan_ns.route('')
@plan_ns.doc(security='Bearer')
class Plans(Resource):
    @jwt_required()
    @plan_ns.expect(request_schema.all())
    def get(self):
        ''' Listar todos los planes '''
        query = request_schema.all().parse_args()
        controller = PlanController()
        return controller.all(query)

    @jwt_required()
    @plan_ns.expect(request_schema.create(), validate=True)
    def post(self):
        ''' Creación de plan '''
        controller = PlanController()
        return controller.create(request.json)


@plan_ns.route('/<int:id>')
@plan_ns.doc(security='Bearer')
class PlansById(Resource):
    @jwt_required()
    def get(self, id):
        ''' Obtener un plan por el ID '''
        controller = PlanController()
        return controller.getById(id)

    @jwt_required()
    @plan_ns.expect(request_schema.update(), validate=True)
    def put(self, id):
        ''' Actualizar un plan por el ID '''
        controller = PlanController()
        return controller.update(id, request.json)

    @jwt_required()
    def delete(self, id):
        ''' Inhabilitar un plan por el ID '''
        controller = PlanController()
        return controller.delete(id)
