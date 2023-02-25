from app import api
from flask_restx import Resource
from app.schemas.favorites_schemas import FavoriteRequestSchema
from flask_jwt_extended import jwt_required
from app.controllers.favorites_controller import FavoriteController
from flask import request
favorites_ns = api.namespace(
    name='Favorites',
    description='Rutas del modelo de Favorites',
    path='/favorites'
)
request_schema=FavoriteRequestSchema(favorites_ns)
@favorites_ns.route('')
@favorites_ns.doc(security='Bearer')
class Favorites(Resource):
    @jwt_required()
    @favorites_ns.expect(request_schema.change(), validate=True)
    def post(self):
        """ Modifica el registro de favorito del producto """
        controller=FavoriteController()
        return controller.change(request.json)

    @jwt_required() 
    def get(self):
        """ Listar todos los favoritos de un usuario """   
        controller=FavoriteController()
        return controller.all() 
""" @favorites_ns.route('/<int:id>')
@favorites_ns.doc(security='Bearer')
class FavoritesById(Resource):
    @jwt_required()
    def delete(self,id):
        controller=FavoriteController()
        return controller.deleteById(id)  """