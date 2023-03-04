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
                'rol_id':1,
                'status': True
             },
             {
               'name':'Luis',
               'last_name':'Lopez',
                'username':'luislopez',
                'password':'123456',
                'email':'luis.lopez@utec.edu.pe',
                'rol_id':2,
                'status': True
             },
             {
               'name':'Brayan',
               'last_name':'Jhonn',
                'username':'bacuna',
                'password':'123456',
                'email':'bj27kn@gmail.com',
                'rol_id':2,
                'status': True
             }
        ]

        for user in users:
            record=UserModel.where(username=user['username']).first()
            if not record:
                print(f'se creo usuario {user}')
                new_record=UserModel.create(**user)
                new_record.hashPassword()
                self.db.session.add(new_record)