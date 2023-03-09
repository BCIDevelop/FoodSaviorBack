from app.models.base import BaseModel
from sqlalchemy import Column,String,Float,Integer,ForeignKey,Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
class PlanModel(BaseModel):

    __tablename__='plans'

    id=Column(Integer,primary_key=True,autoincrement=True)
    price=Column(Float(precision=2))
    name=Column(String)
    