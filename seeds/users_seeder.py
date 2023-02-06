from flask_seeder import Seeder
from app.models.users_model import UserModel

class UserAdminSeeder(Seeder):
    def run(self):
        users=[
            {
               'name':'Usuario',
               'last_name':'Administrador',
                'username':'admin',
                'password':'123456',
                'email':'administrador@gmail.com',
                'rol_id':1
             },
             {
               'name':'Luis',
               'last_name':'Lopez',
                'username':'luislopez',
                'password':'123456',
                'email':'luis.lopez@utec.edu.pe',
                'rol_id':2
             }
        ]

        for user in users:
            record=UserModel.where(username=user['username']).first()
            if not record:
                print(f'se creo usuario {user}')
                new_record=UserModel.create(**user)
                new_record.hashPassword()
                self.db.session.add(new_record)