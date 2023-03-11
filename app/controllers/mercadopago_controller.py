from app.models.orders_model import OrderModel
from app import db
from app.utils.mercadopago import MercadoPago
from app.models.plans_model import PlanModel
from app.controllers.coupons_controller import CouponController
from app.models.coupons_model import CouponModel
""" https://www.mercadopago.com.pe/developers/es/docs/checkout-api/integration-test/test-cards """
class MercadoPagoController:
    def __init__(self) -> None:
        self.model=OrderModel
        self.plan_model=PlanModel
        self.mercadopago=MercadoPago()
        self.coupon=CouponController()
        self.coupon_model=CouponModel
    def updatePaymentStatus(self,payment_id):
        payment=self.mercadopago.getPaymentById(payment_id)
        status=payment['status']
        status_detail=payment['status_detail']
        external_reference=int(payment['external_reference'])

        record=self.model.where(id=external_reference).first()

        if record:
            record.payment_status=status
            record.payment_detail=status_detail
            record.status=status

            db.session.add(record)
            db.session.commit()    
    def createPlan(self,body):
        try:
            plan_id=body["plan_id"]
            record=self.plan_model.where(id=plan_id).first()
            if record:
                 response=self.mercadopago.createPlan(f'Subscripcion Plan {record.name}',record.price)
                 print(response)
                 record.update(mercadopago_id=response["id"])
                 db.session.add(record)
                 db.session.commit()
            return {"message":"Plan not found"},404
        except Exception as e:
                db.session.rollback()
                return {
                    'message': 'Ocurrio un error',
                    'error': str(e)
                }, 500

    def updatePlan(self,body):
            try: 
                
                plan_id=body["mercadopago_plan_id"]
                code=body.get("code")
                if code:
                     record=self.coupon_model.where(code=code,status=True).first()
                     if record:
                        discount=self.coupon._validateDateTimeCouponToPlan(record,code)
                        if discount :
                            print(plan_id)
                            plan_record=self.plan_model.where(mercadopago_id=plan_id,status=True).first()
                            if plan_record:
                                price=plan_record.price*(1-discount)
                                return self.mercadopago.updatePlan(price,plan_id) 
                            return {"message":"Plan not found"},404  
                        return {"message": "Coupon not valid"},400    
                     return {"message":"Code not found"},404   
            except Exception as e:
                db.session.rollback()
                return {
                    'message': 'Ocurrio un error',
                    'error': str(e)
                }, 500 
    
    def listPlans(self,body):
        plan_id=body["mercadopago_plan_id"] 
        return self.mercadopago.listPlan(plan_id)