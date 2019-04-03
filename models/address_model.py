from models.base_model import db
import enum
from sqlalchemy_enum34 import EnumType


class Type(enum.Enum):
    home = 'Home'
    work = 'Work'


class Status(enum.Enum):
    active = 'Active'
    inactive = 'Inactive'


class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    street1 = db.Column(db.String(200), nullable=False)
    street2 = db.Column(db.String(200))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    type = db.Column(EnumType(Type), default=Type.home)
    status = db.Column(EnumType(Status), default=Status.active)
    contact = db.relationship('Contact')
