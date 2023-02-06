from os import getenv
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from flask_seeder import FlaskSeeder
from config import environment

app = Flask(__name__)
app.config.from_object(environment[getenv('ENVIRONMENT')])
CORS(app)

authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    app,
    title='Boilerplate Flask',
    version='0.1',
    description='Endpoints del boilerplate',
    authorizations=authorizations,
    doc='/swagger-ui'
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)
mail = Mail(app)
seeder = FlaskSeeder(app,db)