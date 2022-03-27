from config import db
from sqlalchemy_serializer import SerializerMixin


class Vessel(db.Model, SerializerMixin):
    __tablename__ = 'vessels'

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(8), unique=True)

    def __repr__(self):
        return f'Vessel <{self.code}>'