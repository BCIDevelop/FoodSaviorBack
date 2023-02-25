from app import api
from app.controllers.products_controller import ProductController
from app.schemas.products_schemas import ProductRequestSchema
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from flask import request

product_ns = api.namespace(
    name='Productos',
    description='Rutas del modelo de Productos',
    path='/products'
)

request_schema = ProductRequestSchema(product_ns)

@product_ns.route('')
@product_ns.doc(security='Bearer')
class Products(Resource):
    @jwt_required()
    @product_ns.expect(request_schema.all())
    def get(self):
        """ Listar todos los productos """
        query = request_schema.all().parse_args()
        controller=ProductController()
        return controller.all(query)
    @jwt_required()
    @product_ns.expect(request_schema.create(),validate=True)
    def post(self):
        """ Crear nuevo producto """
        form=request_schema.create().parse_args()
        controller=ProductController()
        return controller.create(form)

@product_ns.route('/<int:id>')
@product_ns.doc(security='Bearer') 
class ProductsById(Resource):
    @jwt_required()
    
    def get(self,id):
        """ Obtener productos por Id """
        controller=ProductController()
        return controller.getById(id)
    @jwt_required()    
    @product_ns.expect(request_schema.update(),validate=True)
    def patch(self,id):
        """ Actualizar producto por Id """
        form=request_schema.update().parse_args()
        data = {key: value for key, value in form.items() if value is not None}
        controller=ProductController()
        return controller.update(id,data)
    @jwt_required()
    def delete(self,id):
        """Eliminar producto por Id """
        controller=ProductController()
        return controller.delete(id)   

@product_ns.route('/user')
@product_ns.doc(security='Bearer') 
class ProductsByUser(Resource):
    @jwt_required()
    @product_ns.expect(request_schema.listByUser())
    def get(self):
        """ Lista todos tus productos """
        query=request_schema.listByUser().parse_args()
        controller=ProductController()
        return controller.getByUser(query) 
    @jwt_required()
    @product_ns.expect(request_schema.createByUser())
    def post(self):
        """ Creacion de un producto del ususario """
        form=request_schema.createByUser().parse_args()
        controller=ProductController()
        return controller.createByUser(form)           