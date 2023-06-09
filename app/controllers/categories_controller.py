
from app.models.categories_model import CategoryModel
from app import db
from app.schemas.categories_schemas import CategoryResponseSchema

class CategoriesController:
    def __init__(self):
        self.model=CategoryModel
        self.schema=CategoryResponseSchema
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

    def getById(self,id):
        try:
           record=self.model.where(id=id).first() #query ---Objeto no se puede enviar por el protocolo HTTP
           if record:
                response=self.schema(many=False) # intacias el serializador 
                return response.dump(record),200 # usar el serializador en el objeto para convertirlo {}
                
           return {
                'message':'No se encuntra la categoria mencionado'
           },404 
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error','error':str(e)
            },500   


    def create(self,data):
        try:
            new_record=self.model.create(**data)
            db.session.add(new_record)
            db.session.commit()
            return {
                'message': f'La categoria {data["name"]} se creo con exito'
            },201
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error','error':str(e)
            },500
    def update(self,id,data):
        try:
            record = self.model.where(id=id).first()
            if record:
                
                record.update(**data)
                db.session.add(record)
                db.session.commit()
                return {
                    'message': f'La categoria {id}, ha sido actualizado'
                },200
            return {
                'message':'No se encuntra La categoria mencionado'
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
                    'message': f'La categoria {id}, ha sido actualizado'
                },200
            return {
                'message':'No se encuntra La categoria mencionado'
            },404
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error','error':str(e)
            },500                        