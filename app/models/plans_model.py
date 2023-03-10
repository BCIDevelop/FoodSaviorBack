from app.models.base import BaseModel
from sqlalchemy import Column,String,Float,Integer,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
class PlanModel(BaseModel):

    __tablename__='plans'

    id=Column(Integer,primary_key=True,autoincrement=True)
    price=Column(Float(precision=2))
    name=Column(String(20))
    mercadopago_id=Column(String(50),nullable=True)
    status=Column(Boolean,default=True)
    