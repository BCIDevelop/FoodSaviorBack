from app import db
from app.models.users_model import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token
from secrets import token_hex
from app.utils.mailing import Mailing
from app.utils.facebook import Facebook

class AuthController:
    def __init__(self):
        self.model = UserModel
        self.rol_id = 2
        self.mailing = Mailing()
        self.facebook= Facebook

    def signIn(self, data):
        try:
            email = data['email']
            password = data['password']
            # 1ª Validar que el usuario exista
            record = self.model.where(email=email).first()
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
                        return {"message":"Contraseña incorrecta"},400
                else:
                    if record.token:
                        return {"message":"Por favor confirma tu cuenta","status":1},403
                    return {"message":"Tu cuenta ha sido inhabilitada por favor comunicate con nostros","status":0},403
            return {
                "message":"No se encontro el ususario"
            },404
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

    def fbLogin(self,data):
        try:
            access_token=data['access_token']
            fb = Facebook(access_token)
            if fb.debugToken() :
                user=fb.getUserInformation()
                email = user['email']
                fb_id = user['id']
                name = user['name']
                avatar = user["picture"]["url"]
                user_data={}
                user_data['fb_id']=fb_id
                user_data['email']=email
                user_data['status']=True
                user_data['rol_id']=2
                user_data['password']=''
                user_data['name']=name
                user_data['avatar']=avatar
                record= self.model.where(email=email).first()
                if not record :
                    new_record = self.model.create(**user_data)
                    db.session.add(new_record)
                    db.session.commit()
                    user_id = new_record.id
                    access_token = create_access_token(identity=user_id)
                    refresh_token = create_refresh_token(identity=user_id)
                    
                else:
                    user_id = record.id
                    access_token = create_access_token(identity=user_id)
                    refresh_token = create_refresh_token(identity=user_id)
                    if not record.fb_id:
                        record.update(fb_id=fb_id)
                        db.session.add(record)
                        db.session.commit()
                       
                return {
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }, 200        
            else:
                return {
                'message': 'Token no valido'
            }, 400

                    
            

        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500