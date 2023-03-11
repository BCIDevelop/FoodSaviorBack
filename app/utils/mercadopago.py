from os import getenv
from requests import post,get,put



class MercadoPago():
    def __init__(self) -> None:
        self.main_token=getenv('MERCADOPAGO_MAIN_ACCESS_TOKEN')
        self.child_token=getenv('MERCADOPAGO_CHILD_ACCESS_TOKEN')
        self.base_url='https://api.mercadopago.com'
        self.url='http://127.0.0.1:5173'
        self.site_id='MPE'
        self.main_headers={
            'Content-Type':'application/json',
            'Authorization':f'Bearer {self.main_token}'
        }
        self.child_headers={
            'Content-Type':'application/json',
            'Authorization':f'Bearer {self.child_token}'
        }

    def createUserTest(self,data):    
        url=f'{self.base_url}/users/test'
        response=post(
            url,
            json={
                'description':data['description'],
                'site_id':self.site_id
            },
            headers=self.main_headers
        )
        return response.json()


     #Creacion subscripcion   
    def createSubscription(self,body):
        print(body)
        url=f'{self.base_url}/preapproval'
        body=body
        response=post(url,json=body,headers=self.child_headers)
        print(response.json())
        return response.json()

    
    # Creacion de plan mercado pago

    def createPlan(self,reason,price):
        url=f'{self.base_url}/preapproval_plan'
        body={
            'reason':reason,
            'back_url':self.url,
            'auto_recurring':{
                "frequency":1,
                "frequency_type":"months",
                "transaction_amount":price,
                "currency_id":"PEN"
            },

            
        }
        response=post(url,json=body,headers=self.child_headers)
        return response.json()
    # Actualizar de plan mercado pago

    def updatePlan(self,new_price,plan_id):
        url=f'{self.base_url}/preapproval_plan/{plan_id}'
        body={
           
            'auto_recurring':{
                "frequency":1,
                "frequency_type":"months",
                "transaction_amount":new_price,
                "currency_id":"PEN"
            },

            
        }
        response=put(url,json=body,headers=self.child_headers)
        
        return response.json()
    def listPlan(self,plan_id):
        url=f'{self.base_url}/preapproval_plan/{plan_id}'
       
        response=get(url,headers=self.child_headers)
        return response.json()

    def getPaymentById(self,id):
        url=f'{self.base_url}/v1/payment/{id}'
        response=get(url)
        return response.json()  