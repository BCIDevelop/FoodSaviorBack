from functools import wraps
from flask_jwt_extended import current_user


def role_required(rol_id):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            role_user = current_user.rol_id
            if role_user == rol_id:
                return fn(*args, **kwargs)
            return {
                'message': 'No cuentas con los permisos suficientes'
            }, 403
        return decorator
    return wrapper
