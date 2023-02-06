from os import getenv
from datetime import timedelta


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = getenv('JWT_SECRET')

    MAIL_SERVER = getenv('MAIL_SERVER')
    MAIL_PORT = getenv('MAIL_PORT')
    MAIL_USE_TLS = getenv('MAIL_USE_TLS')
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')


class DevelopmentConfig(BaseConfig):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=3)
    MAIL_DEBUG = True


class ProductionConfig(BaseConfig):
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)
    MAIL_DEBUG = False
    PROPAGATE_EXCEPTIONS = True


environment = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
