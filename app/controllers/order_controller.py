from app.models.orders_model import OrderModel
from flask_jwt_extended import current_user
from app.models.coupons_model import CouponModel
from app.models.plans_model import PlanModel
from app import db
from app.utils.mercadopago import MercadoPago
from app.models.subscription_model import SubscriptionModel
""" https://www.mercadopago.com.pe/developers/es/docs/checkout-api/integration-test/test-cards """
class OrderController:
    def __init__(self) -> None:
        self.model=OrderModel
        self.coupon_model=CouponModel
        self.plan_model=PlanModel
        self.user_id=current_user.id
        self.mercadopago=MercadoPago()
        self.subscription_model=SubscriptionModel
        
    def create(self,data):
        try:
            print("entro orders")
            coupon=data.get('coupon')
            card_token=data.get('card_token')
            plan_id=data['plan_id']
            print(plan_id)

            plan_record=self.plan_model.where(id=plan_id, status=True).first()
            print(plan_record)
            if not plan_record:
                return {
                    "message":'Plan not Found'
                },404
            prices={
                "subtotal":plan_record.price,
                "discount":0,
                "total":plan_record.price
                
            }
            print(prices)
            if coupon:
                record=self.coupon_model.where(code=coupon).first()
                percentage=record.percentage
                prices["discount"]= 0 if percentage is None else round(prices["subtotal"]*(percentage/100),2)
                prices['total']=round(prices['subtotal']- prices['discount'],2)

            #Creacion del pedido
            order=self.model.create(
                user_id=self.user_id,
                total_price=prices['total'],
                subtotal_price=prices['subtotal'],
                discount_price=prices['discount'],
                code_coupon=coupon
            )
            
            #Crear subscripcion
        
            subscription=self.__createSubscription(plan_record.mercadopago_id,card_token)
            order.subscription_id=subscription["id"]
            subscription_record=self.subscription_model.create(
                    mercadopago_subscription_id=subscription["id"],
                    user_id=self.user_id
            )

            db.session.add(order)
            db.session.add(subscription_record)
            db.session.commit()    
            return {
                'message':'Se creo la subscripcion con exito',
                "result":subscription
                
            },200

        except Exception as e:
            db.session.rollback()
            return {
                'message':'Oops ocurrio un error',
                'error':str(e)
            },500

    def __createSubscription(self,plan_id,card_token):
        print(card_token)
        
        
            
        body={
            "status":"pending",
            "payer_email":current_user.email,
            "preapproval_plan_id":plan_id
        }
        if card_token:
            body["card_token_id"]=card_token
            


        return self.mercadopago.createSubscription(body)