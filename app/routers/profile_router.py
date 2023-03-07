from flask_restx import Resource
from app import api
from flask_jwt_extended import jwt_required
from app.controllers.profile_controller import ProfileController
from app.schemas.profile_schemas import ProfileRequestSchema
profile_ns=api.namespace(
    name="Profile",
    description="Rutas del modelo profile",
    path="/profile",
 )
request_schema=ProfileRequestSchema(profile_ns)
@profile_ns.route('/me')
@profile_ns.doc(security="Bearer")

class Profile(Resource):
    @jwt_required()
    def get(self):
        """ Obtener Perfil de usuario """
        controller=ProfileController()
        return controller.obtain()
    @profile_ns.expect(request_schema.update(),validate=True)
    @jwt_required()
    def patch(self):
        """ Actualizacion parcial del usuario """
        form=request_schema.update().parse_args()
        print(form)
        data = {key: value for key, value in form.items() if value is not None}
        controller=ProfileController()
        return controller.update(data)
    
    @jwt_required()
    def delete(self):
        """ Deshabilitar usuario """
        controller=ProfileController()
        return controller.delete()


    
