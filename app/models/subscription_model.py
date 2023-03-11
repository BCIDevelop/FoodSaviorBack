from app.models.base import BaseModel
from sqlalchemy import Column,String,Integer,ForeignKey

class SubscriptionModel(BaseModel):

    __tablename__='subscriptions'

    id=Column(Integer,primary_key=True,autoincrement=True)
    mercadopago_subscription_id=Column(String(50))
    user_id=Column(Integer,ForeignKey('users.id'))
    