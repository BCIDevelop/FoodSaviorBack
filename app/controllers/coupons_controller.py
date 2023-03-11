from app.models.coupons_model import CouponModel
from app import db
from app.schemas.coupons_schemas import CouponsResponseSchema
from pytz import timezone
from datetime import datetime
class CouponController:
    def __init__(self) -> None:
        self.model=CouponModel
        self.schema=CouponsResponseSchema
        self.timezone=timezone('America/Lima')
        self.datetimenow=datetime.now(tz=self.timezone)
        self.datenow=self.datetimenow.strftime('%Y:%m:%d')
        self.hournow=self.datetimenow.strftime('%H:%M:%S')
    def all(self,query):

        try:
            page=query['page']
            per_page=query['per_page']
            records=self.model.where(status=True).order_by('id').paginate(
                page=page,per_page=per_page
            )

            response= self.schema(many=True)
            return {
                'results':response.dump(records.items),
                'pagination':{
                    'totalRecords':records.total,
                    'totalPages': records.pages,
                    'perPage':records.per_page,
                    'currentPage':records.page
                }

            },200

        except Exception as e:
            return {
                'message': 'Ocurrio un error','error':str(e)
            },500
    def create(self,data):
        try:
            start_date=data["started_at"]
            ended_date=data["ended_at"]
            if self.__validateEndedDateCoupon(ended_date,start_date):

                new_record=self.model.create(**data)
                db.session.add(new_record)
                db.session.commit()
                return {
                    'message': f'El cupon {data["code"]} se creo con exito'
                },201
            return {
                "message":'Por favor revisar las fechas ingresadas'
            },400
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error','error':str(e)
            },500  

    def getById(self,id):
        try:
           record=self.model.where(id=id).first()
           if record:
                response=self.schema(many=False)
                return response.dump(record),200
                
           return {
                'message':'No se encuntra el cupon mencionado'
           },404 
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error','error':str(e)
            },500 
    def update(self,id,data):
        try:
            ended_date=data.get('ended_at')
            record = self.model.where(id=id).first()
            if record:
                started_date=str(record.started_at)
                if self.__validateEndedDateCoupon(ended_date,started_date):
                    record.update(**data)
                    db.session.add(record)
                    db.session.commit()
                    return {
                        'message': f'El cupon {id}, ha sido actualizado'
                    },200
                else:
                    return {
                        "message": 'Por favor revise la fecha ingresada'
                    },400
            return {
                'message':'No se encuntra El cupon mencionado'
            },404
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error','error':str(e)
            },500    
    def delete(self,id):
        try:
            record = self.model.where(id=id).first()
            print(record)
            if record and record.status:
                record.update(status=False)
                db.session.add(record)
                db.session.commit()
                return {
                    'message': f'El cupon {id}, ha sido deshabilitado'
                },200
            return {
                'message':'No se encuntra El cupon mencionado'
            },404
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error','error':str(e)
            },500

    def validate(self,code):
        try:
            record=self.model.where(code=code,status=True).first()
            if record:
                return self._validateDateTimeCoupon(record),200
            return {
                'message':'No se encontro el cupon'
            },404
        except Exception as e:
           
            return {
                'message': 'Ocurrio un error','error':str(e)
            },500

    def __validateEndedDateCoupon(self,ended_date,start_date):   
            if self.datetimenow.isoformat() > ended_date or start_date >= ended_date :
                return False
            return True


    def _validateDateTimeCoupon(self,record):
        started_date=datetime.strftime(record.started_at,'%Y:%m:%d')
        started_hour=datetime.strftime(record.started_at,'%H:%M:%S')

        ended_date=datetime.strftime(record.ended_at,'%Y:%m:%d')
        ended_hour=datetime.strftime(record.ended_at,'%H:%M:%S')
        #Validar las fechas

        if self.datenow < started_date or self.datenow > ended_date:
           raise Exception('El cupon ya vencio o aun no empieza')

        # Validar que estemos en la hora de inicio 
        if self.datenow == started_date and self.hournow < started_hour:
           raise Exception('El cupon aun no puede ser usado')
        # Validar que estemos en la hora de antes de vencer 
        if self.datenow == ended_date and self.hournow > ended_hour:
            raise Exception('El cupon ha vencido')
        response=self.schema(many=False)

        return response.dump(record)
    def _validateDateTimeCouponToPlan(self,record,code):
        record=self.model.where(code=code).first()
        if record:
            started_date=datetime.strftime(record.started_at,'%Y:%m:%d')
            started_hour=datetime.strftime(record.started_at,'%H:%M:%S')

            ended_date=datetime.strftime(record.ended_at,'%Y:%m:%d')
            ended_hour=datetime.strftime(record.ended_at,'%H:%M:%S')
            #Validar las fechas

            if self.datenow < started_date or self.datenow > ended_date:
                return None
            # Validar que estemos en la hora de inicio 
            if self.datenow == started_date and self.hournow < started_hour:
                return None        # Validar que estemos en la hora de antes de vencer 
            if self.datenow == ended_date and self.hournow > ended_hour:
                return None        
            
            return record.percentage

        return None  

