from app.models.base import BaseModel
from sqlalchemy import Column,String,Boolean,Integer,DateTime,Float
class CouponModel(BaseModel):
    __tablename__='coupons'

    id=Column(Integer,primary_key=True,autoincrement=True)
    code=Column(String(50),unique=True)
    percentage=Column(Float(precision=2))
    started_at=Column(DateTime)
    ended_at=Column(DateTime)
    status=Column(Boolean,default=True)