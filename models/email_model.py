from models.base_model import db
import enum
from sqlalchemy_enum34 import EnumType


class Type(enum.Enum):
    personal = 'Personal'
    work = 'Work'


class Email(db.Model):
    __tablename__ = "email"
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    primary = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(100), nullable=False)
    type = db.Column(EnumType(Type))
    contact = db.relationship('Contact')