from app import jwt
from app.models import users_model as model


@jwt.user_lookup_loader
def user_lookup_callback(header, data):
    user = model.UserModel
    identity = data['sub']
    return user.where(id=identity).first()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user or None
