#from app import db

from flask_sqlalchemy import SQLAlchemy
import enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField

db = SQLAlchemy()


class Gender(enum.Enum):
    female = 'Female'
    male = 'Male'
    non_binary = 'Non Binary'


class Race(enum.Enum):
    asian = 'Asian'
    white = 'White'
    black = 'Black'
    hispanic = 'Hispanic/Latino'


class Contact(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email_primary = db.Column(db.String(100), nullable=False)
    phone_primary = db.Column(db.String(25), nullable=False)
    current_profile = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Enum(Gender))
    race_all = db.Column(db.Enum(Race))
    birthdate = db.Column(db.Date)


class ContactSchema(Schema):
    id = fields.Integer(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email_primary = fields.Email(required=True)
    phone_primary = fields.String(required=True)
    current_profile = fields.Integer(required=True)
    gender = EnumField(Gender, by_value=True)
    race_all = EnumField(Race, by_value=True)
    birthdate = fields.DateTime(required=True)
