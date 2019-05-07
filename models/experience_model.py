from models.base_model import db
import enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from sqlalchemy_enum34 import EnumType
from models.achievement_model import Achievement, AchievementSchema

class Type(enum.Enum):
    work = 'Work'
    service = 'Service'
    accomplishment = 'Accomplishment'
    education = 'Education'


class Degree(enum.Enum):
    high_school = 'High School'
    associates = 'Associates'
    undergraduate = 'Undergraduate'
    masters = 'Masters'
    doctoral = 'Doctoral'


class Experience(db.Model):
    __tablename__ = 'experience'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    host = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    degree = db.Column(EnumType(Degree, name='Degree'))
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date)
    type = db.Column(EnumType(Type, name='Type'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

    #relationships
    contact = db.relationship('Contact')
    address = db.relationship('Address')
    achievements = db.relationship('Achievement', back_populates='experience',
                                   cascade='all, delete, delete-orphan')
    resumes = db.relationship('ResumeItem', back_populates='experience',
                              cascade='all, delete, delete-orphan')


class ExperienceSchema(Schema):
    id = fields.Integer()
    description = fields.String()
    host = fields.String(required=True)
    title = fields.String(required=True)
    degree = EnumField(Degree, by_value=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date()
    type = EnumField(Type, by_value=True)
    contact_id = fields.Integer(required=True)
    achievements = fields.Nested(AchievementSchema,
                                 many=True, only=['id', 'description'])
