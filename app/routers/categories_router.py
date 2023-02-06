from app import api
from flask_restx import Resource
from app.schemas.categories_schemas import CategoriesRequestSchema
from app.controllers.categories_controller import CategoriesController
from flask import request
from app.helpers.decorators import role_required
from flask_jwt_extended import jwt_required
categories_ns= api.namespace(
    name='Categories',
    description='Rutas del modelo de categories',
    path='/categories'
)

request_schema=CategoriesRequestSchema(categories_ns)

@categories_ns.route('')
@categories_ns.doc(security='Bearer')
class Category(Resource):
    @jwt_required()
    @categories_ns.expect(request_schema.all())
    def get(self):
        ''' Listar todos las categorias '''
        query_params=request_schema.all().parse_args()
        controller=CategoriesController()
        return controller.all(query_params)

    @categories_ns.expect(request_schema.create(),validate=True)
    @jwt_required()
    @role_required(rol_id=1)
    def post(self):
        '''Creacion de category'''
        controller=CategoriesController()
        return controller.create(request.json)
        
@categories_ns.route('/<int:id>')
@categories_ns.doc(security='Bearer')
class RolesById(Resource):
    '''Obtener category por ID'''
    @jwt_required()
    
    def get(self,id):
        controller=CategoriesController()
        return controller.getById(id)
    @jwt_required()
    @role_required(rol_id=1)    
    @categories_ns.expect(request_schema.update(),validate=True)    
    def put(self,id):
        ''' Actualizar category por ID '''
        controller=CategoriesController()
        return controller.update(id,request.json)
    @jwt_required()
    @role_required(rol_id=1)
    def delete(self,id):
        ''' Eliminar category por ID '''
        print('delete')
        controller=CategoriesController()
        return controller.delete(id)

