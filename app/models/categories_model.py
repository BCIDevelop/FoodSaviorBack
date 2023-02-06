from app.models.base import BaseModel
from sqlalchemy import Column,String,Boolean,Integer
from sqlalchemy.orm import relationship
class CategoryModel(BaseModel):
    __tablename__='categories'

    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(120))
    status=Column(Boolean,default=True)
    products=relationship('ProductModel',uselist=True,back_populates='category')
