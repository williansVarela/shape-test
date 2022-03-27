from sqlalchemy_serializer import SerializerMixin

from config import db


class Equipment(db.Model, SerializerMixin):
    __tablename__ = 'equipments'

    serialize_only = ('id', 'vessel_id', 'name', 'code', 'location', 'active')

    id = db.Column(db.BigInteger, primary_key=True)
    vessel_id = db.Column(db.BigInteger, db.ForeignKey('vessels.id'))
    name = db.Column(db.String(256))
    code = db.Column(db.String(8), unique=True)
    location = db.Column(db.String(256))
    active = db.Column(db.Boolean, server_default='true')

    def __repr__(self):
        return f'Equipment <{self.name} - code: {self.code}>'


class Operation(db.Model, SerializerMixin):
    __tablename__ = 'operations'

    serialize_only = ('id', 'equipment_id', 'type', 'cost')

    id = db.Column(db.BigInteger, primary_key=True)
    equipment_id = db.Column(db.BigInteger, db.ForeignKey('equipments.id'))
    type = db.Column(db.String(32))
    cost = db.Column(db.Float)

    def __repr__(self):
        return f'Operation <{self.id} - code: {self.equipment_id.code}>'
