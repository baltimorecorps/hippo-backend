from models.base_model import db
import enum
from marshmallow import Schema, fields, EXCLUDE
from marshmallow_enum import EnumField


class Type(enum.Enum):
    personal = 'Personal'
    work = 'Work'


class Email(db.Model):
    __tablename__ = 'email'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(Type, name='EmailType'))

    #relationships
    contact = db.relationship('Contact', back_populates='email_primary')


class EmailSchema(Schema):
    id = fields.Integer(dump_only=True)
    is_primary = fields.Boolean()
    email = fields.Email(required=True)
    type = EnumField(Type, by_value=True)

    class Meta:
        unknown = EXCLUDE
