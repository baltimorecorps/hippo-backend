from models.base_model import db
import enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from models.achievement_model import Achievement, AchievementSchema
from sqlalchemy.ext.hybrid import hybrid_property

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
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date)
    type = db.Column(db.Enum(Type, name='ExperienceType'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

    #relationships
    contact = db.relationship('Contact')
    address = db.relationship('Address')
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
            delta = dt.datetime.today() - self.date_start

        else:
            delta = self.date_end - self.date_start
        months = delta.month
        return f'{math.floor(months/12)},  {months % 12}'

class ExperienceSchema(Schema):
    id = fields.Integer(dump_only=True)
    description = fields.String()
    host = fields.String(required=True)
    title = fields.String(required=True)
    degree = EnumField(Degree, by_value=True)
    start_month = fields.String(required=True)
    end_month = fields.String()
    start_year = fields.Integer(required=True)
    end_year = fields.Integer()
    date_length = fields.String(dump_only=True)
    type = EnumField(Type, by_value=True)
    contact_id = fields.Integer(required=True)
    achievements = fields.Nested(AchievementSchema, many=True)
