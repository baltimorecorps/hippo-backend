from flask_sqlalchemy import SQLAlchemy
import enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from sqlalchemy_enum34 import EnumType
from models.contact_model import Contact

db = SQLAlchemy()


class Type(enum.Enum):
    work = 'Work'
    service = 'Service'
    accomplishment = 'Accomplishment'
    education = 'Education'


class Experience(db.Model):
    __tablename__ = "experience"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    host = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date)
    type = db.Column(EnumType(Type))
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)


class ExperienceSchema(Schema):
    id = fields.Integer()
    description = fields.String()
    host = fields.String(required=True)
    title = fields.String(required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date()
    type = EnumField(Type, by_value=True)
    contact_id = fields.Integer()