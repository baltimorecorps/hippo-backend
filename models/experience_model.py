from models.base_model import db
import enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from models.achievement_model import Achievement, AchievementSchema
from sqlalchemy.ext.hybrid import hybrid_property
import datetime as dt
import math

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
    degree = db.Column(db.Enum(Degree, name='Degree'))
    start_month = db.Column(db.String(100), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_month = db.Column(db.String(100))
    end_year = db.Column(db.Integer)
    type = db.Column(db.Enum(Type, name='ExperienceType'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    location_city = db.Column(db.String(100))
    location_state = db.Column(db.String(100))

    #relationships
    contact = db.relationship('Contact')
    achievements = db.relationship('Achievement', back_populates='experience',
                                   cascade='all, delete, delete-orphan')
    resumes = db.relationship('ResumeItem', back_populates='experience',
                              cascade='all, delete, delete-orphan')

    #calculated fields
    @hybrid_property
    def start_month(self):
        try:
            return self.date_start.strftime('%B')
        except AttributeError:
            return None

    @hybrid_property
    def start_year(self):
        try:
            return self.date_start.strftime('%Y')
        except AttributeError:
            return None

    @hybrid_property
    def end_month(self):
        try:
            return self.date_end.strftime('%B')
        except AttributeError:
            return None

    @hybrid_property
    def end_year(self):
        try:
            return self.date_end.strftime('%Y')
        except AttributeError:
            return None

    @hybrid_property
    def date_length(self):
        if not self.date_end:
            delta = ((dt.datetime.today().year - self.date_start.year) * 12
                      + dt.datetime.today().month - self.date_start.month)
        else:
            delta = ((self.date_end.year - self.date_start.year) * 12
                      + self.date_end.month - self.date_start.month)
        return delta

    @hybrid_property
    def length_year(self):
        return math.floor(self.date_length/12)

    @hybrid_property
    def length_month(self):
        return self.date_length % 12

class ExperienceSchema(Schema):
    id = fields.Integer(dump_only=True)
    description = fields.String()
    host = fields.String(required=True)
    title = fields.String(required=True)
    degree = EnumField(Degree, by_value=True, missing=None)
    current_experience = fields.Boolean()
    start_month = fields.String(required=True)
    start_year = fields.Integer(required=True)
    end_month = fields.String()
    end_year = fields.Integer()
    length_year = fields.Integer(dump_only=True)
    length_month = fields.Integer(dump_only=True)
    type = EnumField(Type, by_value=True)
    contact_id = fields.Integer(required=True)
    location_city = fields.String()
    location_state = fields.String()
    achievements = fields.Nested(AchievementSchema, many=True)
