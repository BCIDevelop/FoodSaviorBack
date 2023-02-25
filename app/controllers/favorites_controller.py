from app.models.favorites_model import FavoriteModel
from app.schemas.favorites_schemas import FavoriteResponseSchema
from flask_jwt_extended import current_user
from app import db
from app.models.products_model import ProductModel
class FavoriteController:
    def __init__(self) -> None:
        self.model=FavoriteModel
        self.schema=FavoriteResponseSchema
        self.user=current_user.id
        self.product_model=ProductModel
    def change(self,data):
        try:
            product_id=data["product_id"]
            record=self.product_model.where(id=product_id,user_id=self.user).first()
            if not record:
                return {"message": f'El producto {product_id} no existe para tu usuario'},404
            data["user_id"]=self.user
            record_favorite=self.model.where(product_id=product_id).first()
            if not record_favorite:
                new_record=self.model.create(**data)
                db.session.add(new_record)
                db.session.commit()
                return {
                "message":f"El product {product_id} se agrego como favorito "
                },201
            record_favorite.delete()   
            db.session.commit()
            return {},204

            
        except Exception as e:
            db.session.rollback()
            return {
                    'message': 'Ocurrio un error',
                    'error': str(e)
            }, 500

    """ def deleteById(self,id):
        try:
            
            record=self.model.where(id=id).first()
            if not record:
                return {"message":'Favorite record not found'},404
            record.delete()
            db.session.commit()
            return {},204
        except Exception as e:
            db.session.rollback()
            return {
                    'message': 'Ocurrio un error',
                    'error': str(e)
            }, 500 """
    def all(self):
        try:
            
            records=self.model.where(user_id=self.user).all()
            response=self.schema(many=True)
            
            return {
                'results':response.dump(records)
            },200
        except Exception as e:
            return {
                    'message': 'Ocurrio un error',
                    'error': str(e)
            }, 500    