from models.base_model import db
import enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from sqlalchemy_enum34 import EnumType
from models.experience_model import Experience, ExperienceSchema, Type


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
    work_experience = db.relationship("Experience",
                                      primaryjoin=db.and_(id == Experience.contact_id, Experience.type == Type.work),
                                      back_populates='contact')
    education_experience = db.relationship("Experience",
                                      primaryjoin=db.and_(id == Experience.contact_id, Experience.type == Type.education),
                                      back_populates='contact')
    service_experience = db.relationship("Experience",
                                      primaryjoin=db.and_(id == Experience.contact_id, Experience.type == Type.service),
                                      back_populates='contact')
    accomplishment_experience = db.relationship("Experience",
                                      primaryjoin=db.and_(id == Experience.contact_id, Experience.type == Type.accomplishment),
                                      back_populates='contact')

    def __init__(self, id, first_name, last_name, email_primary, phone_primary, current_profile, gender, race_all, birthdate, salutation, work_experience, education_experience, service_experience, accomplishment_experience):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email_primary = email_primary
        
    def toString(self):
        return 'Id: {}, First Name: {}'.format(self.id, self.first_name)

# 'First Name': self.first_name, 'Last Name': self.last_name, 'Primary Email': self.email_primary}


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


class ProfileSchema(Schema):
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
    work_experience = fields.List(fields.Nested(ExperienceSchema))
    education_experience = fields.List(fields.Nested(ExperienceSchema))
    service_experience = fields.List(fields.Nested(ExperienceSchema))
    accomplishment_experience = fields.List(fields.Nested(ExperienceSchema))
