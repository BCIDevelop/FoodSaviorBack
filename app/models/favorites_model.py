from app.models.base import BaseModel
from sqlalchemy import Column,Integer,ForeignKey
from sqlalchemy.orm import relationship

class FavoriteModel(BaseModel):
    __tablename__='favorites'

    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    product_id=Column(Integer,ForeignKey('products.id'))
    product=relationship('ProductModel',uselist=False,back_populates='favorite')
    user=relationship('UserModel',uselist=False,back_populates='favorites')