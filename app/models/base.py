from app import db
from sqlalchemy_mixins import AllFeaturesMixin


class BaseModel(db.Model, AllFeaturesMixin):
    __abstract__ = True
