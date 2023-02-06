from app import db
from app.models.roles_model import RoleModel
from app.schemas.roles_schemas import RolesResponseSchema


class RolesController:
    def __init__(self):
        self.model = RoleModel
        self.schema = RolesResponseSchema

    def all(self, query):
        try:
            page = query['page']
            per_page = query['per_page']

            # Paginate
            # page -> Pagina actual
            # per_page -> Total de registros x pagina
            # total -> Total de registros
            # pages -> Total de paginas
            # items -> Lista de objetos
            records = self.model.where(status=True).order_by('id').paginate(
                page=page, per_page=per_page
            )
            response = self.schema(many=True)
            return {
                'results': response.dump(records.items),
                'pagination': {
                    'totalRecords': records.total,
                    'totalPages': records.pages,
                    'perPage': records.per_page,
                    'currentPage': records.page
                }
            }, 200
        except Exception as e:
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500

    def getById(self, id):
        try:
            record = self.model.where(id=id).first()
            if record:
                response = self.schema(many=False)
                return response.dump(record), 200
            return {
                'message': 'No se encontro el rol mencionado'
            }, 404
        except Exception as e:
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500

    def create(self, data):
        try:
            new_record = self.model.create(**data)
            db.session.add(new_record)
            db.session.commit()
            return {
                'message': f'El rol {data["name"]} se creo con exito'
            }, 201
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500

    def update(self, id, data):
        try:
            record = self.model.where(id=id).first()
            if record:
                record.update(**data)
                db.session.add(record)
                db.session.commit()
                return {
                    'message': f'El rol {id}, ha sido actualizado'
                }, 200
            return {
                'message': 'No se encontro el rol mencionado'
            }, 404
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500

    def delete(self, id):
        try:
            record = self.model.where(id=id).first()
            if record and record.status:
                record.update(status=False)
                db.session.add(record)
                db.session.commit()
                return {
                    'message': f'El rol {id}, ha sido deshabilitado'
                }, 200
            return {
                'message': 'No se encontro el rol mencionado'
            }, 404
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500
