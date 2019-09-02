from models.base_model import db
import enum
from sqlalchemy_enum34 import EnumType
from marshmallow import Schema, fields
from marshmallow_enum import EnumField

class Type(enum.Enum):
    home = 'Home'
    work = 'Work'


class Status(enum.Enum):
    active = 'Active'
    inactive = 'Inactive'


class Address(db.Model):
    __tablename__ = 'address'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    street1 = db.Column(db.String(200), nullable=False)
    street2 = db.Column(db.String(200))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    type = db.Column(db.Enum(Type, name='AddressType'), default=Type.home)
    status = db.Column(db.Enum(Status, name='Status'), default=Status.active)

    #relationships
    contact = db.relationship('Contact', back_populates='addresses')


class AddressSchema(Schema):
    id = fields.Integer()
    is_primary = fields.Boolean()
    street1 = fields.String(required=True)
    street2 = fields.String()
    city = fields.String(required=True)
    state = fields.String(required=True)
    country = fields.String(required=True)
    postal_code = fields.String(required=True)
    type = EnumField(Type, by_value=True)
    status = EnumField(Status, by_value=True)
