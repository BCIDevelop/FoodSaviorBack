from app import db
from app.models.users_model import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token
from secrets import token_hex
from app.utils.mailing import Mailing


class AuthController:
    def __init__(self):
        self.model = UserModel
        self.rol_id = 2
        self.mailing = Mailing()

    def signIn(self, data):
        try:
            username = data['username']
            password = data['password']

            # 1ª Validar que el usuario exista
            record = self.model.where(username=username).first()
            if record:
                if record.status:
                    # 2ª Validar que la contraseña sea correcta
                    if record.checkPassword(password):
                        # 3º Creación de JWT (Access Token y Refresh Token)
                        user_id = record.id
                        access_token = create_access_token(identity=user_id)
                        refresh_token = create_refresh_token(identity=user_id)
                        return {
                            'access_token': access_token,
                            'refresh_token': refresh_token
                        }, 200
                    else:
                        raise Exception('La contraseña es incorrecta')
                else:
                    if record.token:
                        return {"message":"Por favor confirma tu cuenta","status":1},403
                    return {"message":"Tu cuenta ha sido inhabilitada por favor comunicate con nostros","status":0},403
            raise Exception('No se encontro el usuario')
        except Exception as e:
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500

    def signUp(self, data):
        try:
            # Ingresar o insertar el rol_id
            data['rol_id'] = self.rol_id
            email=data["email"]
            name=data["name"]
            token=token_hex(5)
            data['token']=token   
            new_record = self.model.create(**data)
            new_record.hashPassword()
            self.mailing.emailConfirmAccount(
                    email,name,token
            )
            db.session.add(new_record)
            db.session.commit()

            return {
                'message': 'El usuario se creo con exito'
            }, 201
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500

    def refreshToken(self, identity):
        try:
            access_token = create_access_token(identity=identity)
            return {
                'access_token': access_token
            }, 200
        except Exception as e:
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500

    def resetPassword(self, data):
        try:
            email = data['email']
            record = self.model.where(email=email).first()
            if record:
                new_password = token_hex(5)
                record.password = new_password
                record.hashPassword()

                self.mailing.emailResetPassword(
                    record.email, record.name, new_password
                )

                db.session.add(record)
                db.session.commit()
                return {
                    'message': 'Se envio un correo con tu nueva contraseña'
                }, 200
            return {
                'message': 'No se encontro el usuario mencionado'
            }, 404
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500

    def claimAccount(self,query):
        try:
            email=query["email"]
            token=query["token"]
            print(query)
            record=self.model.where(email=email).first()
            if not record:
                return {"message":"Usuario no registrado"},404
            if record.status==True:
                return {"message":"Usuario ya esta activo"},400
            if record.token!=token:
                return {"message":"token no valido"},400
            record.update(status=True,token=None)
            db.session.add(record)
            db.session.commit()
            return {},204
        except Exception as e:
            db.session.rollback()
            
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500
