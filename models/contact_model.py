from models.base_model import db
import enum
from marshmallow import Schema, fields, EXCLUDE
from marshmallow_enum import EnumField
from models.experience_model import Experience, ExperienceSchema, Type
from models.email_model import Email, EmailSchema
from models.address_model import Address
from models.achievement_model import Achievement

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
    __tablename__ = 'contact'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    salutation = db.Column(db.Enum(Salutation, name='Salutation'))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_primary = db.Column(db.String(25))
    gender = db.Column(db.Enum(Gender, name='Gender'))
    race_all = db.Column(db.Enum(Race, name='Race'))
    birthdate = db.Column(db.Date)

    #relationships
    emails = db.relationship('Email', back_populates='contact')
    email_primary = db.relationship("Email",
                                    primaryjoin=db.and_(id == Email.contact_id,
                                                        Email.is_primary == True),
                                    uselist=False)
    addresses = db.relationship('Address', back_populates='contact')
    address_primary = db.relationship('Address',
                                      primaryjoin=db.and_(id == Address.contact_id, Address.is_primary == True),
                                      back_populates='contact',
                                      uselist=False)
    achievements = db.relationship('Achievement', back_populates='contact',
                                   cascade='all, delete, delete-orphan')
    resumes = db.relationship('Resume', back_populates='contact',
                              cascade='all, delete, delete-orphan')
    tags = db.relationship('TagItem', back_populates='contact',
                           cascade='all, delete, delete-orphan')
    experiences = db.relationship('Experience', back_populates='contact',
                                  cascade='all, delete, delete-orphan')

class ContactSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email_primary = fields.Nested(EmailSchema)
    emails = fields.Nested(EmailSchema, many=True)
    phone_primary = fields.String()
    gender = EnumField(Gender, by_value=True, missing=None)
    race_all = EnumField(Race, by_value=True, missing=None)
    birthdate = fields.Date(allow_none=True)

    class Meta:
        unknown = EXCLUDE
