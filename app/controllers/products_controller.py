from app.models.products_model import ProductModel
from app.schemas.products_schemas import ProductResponseSchema
from app import db
from app.utils.bucket import Bucket
from flask_jwt_extended import current_user
from datetime import datetime
from sqlalchemy import or_
from os import getenv
class ProductController:
    def __init__(self) -> None:
        self.model=ProductModel
        self.schema=ProductResponseSchema
        self.bucket_folder = "products"
        self.__validUnits=['KG','UNI']
        self.bucket=Bucket( getenv('AWS_BUCKET_NAME'), self.bucket_folder)
        self.user=current_user.id
        self.__allowed_extensions=['png','jpg','jpeg','gif']
        self.now=datetime.now()
        
    def all(self,query):
        try:
           page=query['page']
           per_page=query['per_page']
           records=self.model.query.order_by('id').paginate(
                page=page,per_page=per_page
            )   
           response=self.schema(many=True)
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

    def create(self,form):
        try:
            unit=form['unit']
            image=form['image']
            spoildate=form['spoilDate']
            #Validation
            self.__validateUnits(unit)
            self.__validateSpoilDate(spoildate)
            name,stream=self.__validateExtensionImage(image)
            #Adding a string to make filename unique
            file_name=self.__addSugar(name)
            url=self.bucket.uploadObject(file_name,stream)
            form['image']=url 
            form['created_at']=self.now
            new_record=self.model.create(**form)
            db.session.add(new_record)
            db.session.commit()
            return {
                'message':f'El producto {form["name"]} se creo con exito'
            },201
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error','error':str(e)
            },500   
    def getById(self,id): 
        try:
            record=self.model.where(id=id).first()   
            if not record:
                return {
                    'message': 'No se encontro el producto mencionado'
                },404
            response=self.schema(many=False)
            return response.dump(record),200    
        except Exception as e:
            return {
                    'message': 'Ocurrio un error',
                    'error': str(e)
            }, 500    
    def update(self,id,data):
        try:
            record=self.model.where(id=id).first()   
            
            if not record:
                return {
                    'message': 'No se encontro el producto mencionado'
                },404
            image=data.get('image')
            unit=data.get('unit')
            spoil_date=data.get('spoilDate')    
            if spoil_date:
                self.__validateSpoilDate(spoil_date)
            if image:
                name,stream=self.__validateExtensionImage(image)
                file_name=record.image.split('products/')[1]
                new_url=self.bucket.uploadObject(file_name,stream)
                data['image']=new_url
            if unit:
                self.__validateUnits(unit)    
            record.update(**data)    
            db.session.add(record)
            db.session.commit()
            return {'message':'El producto se actualizo con exito'},200
        except Exception as e:
            db.session.rollback()
            return {
                    'message': 'Ocurrio un error',
                    'error': str(e)
            }, 500

    def delete(self,id):
        try:
            record=self.model.where(id=id).first()
            if not record:
                return {
                    'message': 'No se encontro el producto mencionado'
                },404
            file_name=record.image.split('products/')[1]  
            self.bucket.deleteObject(file_name)
            record.delete()
            db.session.commit()
            return {'message':'Se elimino el producto con exito'},200
        except Exception as e:
            db.session.rollback()
            return {
                    'message': 'Ocurrio un error',
                    'error': str(e)
            }, 500    
    def getByUser(self,query):
        try:
            filters={}
            page=query['page']
            per_page=query['per_page']
            if query['q']:
                filters = {
                    or_: {
                        'name__ilike': f"%{query['q']}%",
                        'description__ilike': f"%{query['q']}%"
                    }
                }

            if query['category_id']:
                filters['category_id']=query['category_id']   

            ordering = ['spoilDate'] if query['ordering_by_spoilDate'] is not None and query['ordering_by_spoilDate']==1 else ['id']
                
            filters['user_id']=self.user
            records=self.model.smart_query(
                filters={**filters},
                sort_attrs=ordering
            ).paginate(page=page,per_page=per_page)
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
                    'message': 'Ocurrio un error',
                    'error': str(e)
            }, 500

    def createByUser(self,form):
        print(form)
        try:
            unit=form['unit']
            image=form['image']
            spoildate=form['spoilDate']
            #Validation
            self.__validateUnits(unit)
            self.__validateSpoilDate(spoildate)
            name,stream=self.__validateExtensionImage(image)
            #Adding a string to make filename unique
            file_name=self.__addSugar(name)
            url=self.bucket.uploadObject(file_name,stream)
            form['image']=url 
            form['created_at']=self.now
            form['user_id']=self.user
            new_record=self.model.create(**form)
            db.session.add(new_record)
            db.session.commit()
            return {
                'message':f'El producto {form["name"]} se creo con exito'
            },201
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error','error':str(e)
            },500              
    def __validateExtensionImage(self,obj_image):
        filename=obj_image.filename
        stream=obj_image.stream
        extension=filename.split('.')[1]
        if extension.lower() not in self.__allowed_extensions:
            raise Exception('El tipo de archivo usado, no esta permitido')

        return filename,stream    


    def __validateUnits(self,unit):
        if unit not in self.__validUnits:
            raise Exception('Unidad no permitida por favor ingrese la unidad nuevamente')   

    def __validateSpoilDate(self,date):
        print(self.now.strftime("%m-%d-%Y"))
        print(date.strftime("%m-%d-%Y"))
        if date.strftime("%m-%d-%Y") <= self.now.strftime("%m-%d-%Y"):
            raise Exception('Este producto ya vencio o vence hoy dia')   

    def __addSugar(self,name):
        file_name_array=name.split('.')
        string_sugar=f'{self.now.strftime("%m-%d-%YT%H%M%S")}.'
        file_name_array.insert(1,string_sugar)
        file_name=''.join(file_name_array)
        return f'{self.user}/{file_name}'