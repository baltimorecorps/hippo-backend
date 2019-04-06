from models.base_model import db
import enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from sqlalchemy_enum34 import EnumType
from models.experience_model import Experience, ExperienceSchema, Type
from models.email_model import Email, EmailSchema
from models.address_model import Address, AddressSchema

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
    salutation = db.Column(EnumType(Salutation))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.relationship("Email",
                            primaryjoin=(id == Email.contact_id),
                            back_populates='contact')
    email_primary = db.relationship("Email",
                                    primaryjoin=db.and_(id == Email.contact_id, Email.is_primary == True),
                                    back_populates='contact',
                                    uselist=False)
    address = db.relationship("Address",
                              primaryjoin=(id == Address.contact_id),
                              back_populates='contact')
    address_primary = db.relationship("Address",
                                      primaryjoin=db.and_(id == Address.contact_id, Address.is_primary == True),
                                      back_populates='contact',
                                      uselist=False)
    phone_primary = db.Column(db.String(25))
    gender = db.Column(EnumType(Gender))
    race_all = db.Column(EnumType(Race))
    birthdate = db.Column(db.Date)
    work_experience = db.relationship("Experience",
                                      primaryjoin=db.and_(id == Experience.contact_id, Experience.type == Type.work),
                                      order_by=(Experience.date_end.desc(), Experience.date_start.desc()),
                                      back_populates='contact')
    education_experience = db.relationship("Experience",
                                           primaryjoin=db.and_(id == Experience.contact_id, Experience.type ==
                                                               Type.education),
                                           order_by=(Experience.date_end.desc(), Experience.date_start.desc()),
                                           back_populates='contact')
    service_experience = db.relationship("Experience",
                                         primaryjoin=db.and_(id == Experience.contact_id, Experience.type ==
                                                             Type.service),
                                         order_by=(Experience.date_end.desc(), Experience.date_start.desc()),
                                         back_populates='contact')
    accomplishment_experience = db.relationship("Experience",
                                                primaryjoin=db.and_(id == Experience.contact_id, Experience.type ==
                                                                    Type.accomplishment),
                                                order_by=(Experience.date_end.desc(), Experience.date_start.desc()),
                                                back_populates='contact')


class ContactAllSchema(Schema):
    id = fields.Integer()
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email_primary = fields.Nested(EmailSchema)

class ContactOneSchema(Schema):
    id = fields.Integer()
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email_primary = fields.Nested(EmailSchema)
    phone_primary= fields.String()
    gender = EnumField(Gender, by_value=True)
    race_all = EnumField(Race, by_value=True)
    birthdate = fields.Date()

class ProfileSchema(Schema):
    id = fields.Integer()
    salutation = EnumField(Salutation, by_value=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email_primary = fields.Email(required=True)
    phone_primary = fields.String()
    gender = EnumField(Gender, by_value=True)
    race_all = EnumField(Race, by_value=True)
    birthdate = fields.Date()
    work_experience = fields.List(fields.Nested(ExperienceSchema))
    education_experience = fields.List(fields.Nested(ExperienceSchema))
    service_experience = fields.List(fields.Nested(ExperienceSchema))
    accomplishment_experience = fields.List(fields.Nested(ExperienceSchema))
