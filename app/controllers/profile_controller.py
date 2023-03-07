
from app.models.users_model import UserModel
from flask_jwt_extended import current_user
from app.schemas.profile_schemas import ProfileResponseSchema
from app.utils.bucket import Bucket
from app import db

class ProfileController:
    def __init__(self) -> None:
        self.model=UserModel
        self.user=current_user.id
        self.schema=ProfileResponseSchema
        self.__allowed_extensions=['png','jpg']  
        self.bucket=Bucket('food-savior','avatar')
    def obtain(self):
        try:
            record=self.model.where(id=self.user).first()
            response=self.schema(many=False)
            return {
                "result":response.dump(record)
            },200
        except Exception as e:
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500
    def delete(self):
        try:
            record=self.model.where(id=self.user).first()
            if record.status == True:
                record.update(status=False)
                db.session.add(record)
                db.session.commit()
                return {},204
            return {
                "message":"User not found",
            },404    
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500    

    def update(self,form):
        try:
            print(form)
            password=form.get("password")
            confirm_password=form.get("confirm_password")
            print(form)
            image=form.get("avatar")
            username=form.get("username")
            record=self.model.where(id=self.user).first()
            
            if password: 
                if password == confirm_password: 
                    form.pop("confirm_password")
                else:
                    return {"message": "Password doesnt match"},400

            if image:
                stream=self.__validateExtensionImage(image)
                url=self.bucket.uploadObject(self.user,stream)
                form["avatar"]=url

            if username and username != record.username:
                username_record=self.model.where(username=username).first()
                if username_record:
                    return {"message":"Username already exist"},400
            
            record.update(**form)
            record.hashPassword()
            db.session.add(record)
            db.session.commit()
            return {
                "message":"User succesfully modified"
            },200



                

        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Ocurrio un error',
                'error': str(e)
            }, 500           
        
    def __validateExtensionImage(self,obj_image):
        filename=obj_image.filename
        stream=obj_image.stream
        extension=filename.split('.')[1]
        if extension.lower() not in self.__allowed_extensions:
            raise Exception('El tipo de archivo usado, no esta permitido')

        return stream         