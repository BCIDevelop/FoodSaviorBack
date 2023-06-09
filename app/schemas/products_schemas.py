from app.models.products_model import ProductModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_restx.reqparse import RequestParser
from werkzeug.datastructures import FileStorage
from flask_restful import inputs
from marshmallow.fields import Nested 
class ProductRequestSchema:
    def __init__(self,namespace) -> None:
        self.namespace=namespace
    

    def all(self):
        parser= RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        return parser

    def create(self):
        parser=RequestParser()
        parser.add_argument('name',type=str,required=True,location='form')
        parser.add_argument('description',type=str,required=True,location='form')
        parser.add_argument('unit',type=str,required=True,location='form',choices=('UNI', 'KG'))
        parser.add_argument('image',type=FileStorage,required=True,location='files')
        parser.add_argument('category_id',type=int,required=True,location='form')
        parser.add_argument('user_id',type=int,required=True,location='form')
        parser.add_argument('spoilDate',type=inputs.date,required=True,help='Formato Date como 2007-11-03',location='form')  
        parser.add_argument('barcode',type=str,required=True,location='form')  
        return parser
    def update(self):
        parser=RequestParser()
        parser.add_argument('name',type=str,required=False,location='form')
        parser.add_argument('description',type=str,required=False,location='form')
        parser.add_argument('unit',type=str,required=False,location='form',choices=('UNI', 'KG'))
        parser.add_argument('image',type=FileStorage,required=False,location='files')
        parser.add_argument('category_id',type=int,required=False,location='form')
        parser.add_argument('spoilDate',type=inputs.date,required=False,help='Formato Date como 2007-11-03',location='form')  
        parser.add_argument('barcode',type=str,required=False,location='form')    
        
        return parser
    def listByUser(self):
        parser=RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')
        parser.add_argument('q',type=str,required=False,location='args')        
        parser.add_argument('ordering_by_spoilDate',type=int,required=False,location='args',help='If 1 will order the products by its spoil Date')        
        parser.add_argument('category_id',type=int,required=False,location='args')        
        return parser
    def createByUser(self):
        parser=RequestParser()
        parser.add_argument('name',type=str,required=True,location='form')
        parser.add_argument('description',type=str,required=True,location='form')
        parser.add_argument('unit',type=str,required=True,location='form',choices=('UNI', 'KG'))
        parser.add_argument('image',type=FileStorage,required=True,location='files')
        parser.add_argument('category_id',type=int,required=True,location='form')
        parser.add_argument('spoilDate',type=inputs.date,required=True,help='Formato Date como 2007-11-03',location='form')  
        parser.add_argument('barcode',type=str,required=True,location='form')  
        return parser
class ProductResponseSchema(SQLAlchemyAutoSchema):
  
    class Meta:
        model = ProductModel
        ordered = True
    category = Nested('CategoryResponseSchema', exclude=['id','status'], many=False)
