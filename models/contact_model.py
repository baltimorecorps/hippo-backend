from flask_sqlalchemy import SQLAlchemy
import enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from sqlalchemy_enum34 import EnumType

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


class Salutation(enum.Enum):
    miss = 'Miss'
    mrs = 'Mrs.'
    mr = 'Mr.'
    ms = 'Ms.'
    dr = 'Dr.'


class Contact(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email_primary = db.Column(db.String(100), nullable=False)
    phone_primary = db.Column(db.String(25))
    current_profile = db.Column(db.Integer)
    gender = db.Column(EnumType(Gender))
    race_all = db.Column(EnumType(Race))
    birthdate = db.Column(db.Date, nullable=False)
    salutation = db.Column(EnumType(Salutation))



class ContactSchema(Schema):
    id = fields.Integer()
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email_primary = fields.Email(required=True)
    phone_primary = fields.String()
    current_profile = fields.Integer()
    gender = EnumField(Gender, by_value=True)
    race_all = EnumField(Race, by_value=True)
    birthdate = fields.Date(required=True)
    salutation = EnumField(Salutation, by_value=True)
