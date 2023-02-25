from app.models.base import BaseModel
from sqlalchemy import Column,String,Integer,Text,ForeignKey,DateTime
from sqlalchemy.orm import relationship

class ProductModel(BaseModel):
    __tablename__='products'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(100))
    description=Column(Text)
    image=Column(String(255))
    category_id=Column(Integer,ForeignKey('categories.id'))
    user_id=Column(Integer,ForeignKey('users.id'))
    unit=Column(String(40))
    spoilDate=Column(DateTime)
    
    barcode=Column(String(20))
    created_at=Column(DateTime)
    category= relationship('CategoryModel',uselist=False,back_populates='products')
    favorite= relationship('FavoriteModel',uselist=False,back_populates='product')
    user= relationship('UserModel',uselist=False,back_populates='products')
