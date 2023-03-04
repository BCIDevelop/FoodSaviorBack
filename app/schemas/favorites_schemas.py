from flask_restx import fields
from marshmallow.fields import Nested
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.favorites_model import FavoriteModel

class FavoriteRequestSchema:
    def __init__(self,namespace) -> None:
        self.namespace=namespace

    def change(self):
         return self.namespace.model('Favorite Change', {
            'product_id': fields.Integer(required=True)
        })
    def changeBulk(self):
         return self.namespace.model('Favorite Change Bulk', {
            'products': fields.List((fields.Integer),required=True)
        })
class FavoriteResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FavoriteModel
        ordered = True

    product = Nested('ProductResponseSchema', exclude=['description'], many=False)
    