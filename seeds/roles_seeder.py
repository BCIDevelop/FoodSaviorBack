from flask_seeder import Seeder
from app.models.roles_model import RoleModel

class RoleSeeder(Seeder):
    def run(self):
        roles = [
            {
            'name':'Administrador',
        },
        {
            'name': 'Usuario Normal'            
        }
        ]

        for role in roles:
            record=RoleModel.where(name=role['name']).first()
            if not record:
                print(f'se crea rol: {role}')
                new_record=RoleModel.create(**role)
                self.db.session.add(new_record)

