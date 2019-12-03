from models.base_model import db
import enum
from marshmallow import Schema, fields, EXCLUDE
from marshmallow_enum import EnumField
from models.achievement_model import Achievement, AchievementSchema
from models.skill_model import experience_skills, SkillItemSchema
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

class Month(enum.Enum):
    none = 'none'
    january = 'January'
    february = 'February'
    march = 'March'
    april = 'April'
    may = 'May'
    june = 'June'
    july = 'July'
    august = 'August'
    september = 'September'
    october = 'October'
    november = 'November'
    december = 'December'


class Experience(db.Model):
    __tablename__ = 'experience'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    host = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    degree_other = db.Column(db.String(100))
    degree = db.Column(db.String(100))
    link = db.Column(db.String(255))
    start_month = db.Column(db.Enum(Month, name='MonthType'), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_month = db.Column(db.Enum(Month, name='MonthType'), nullable=False)
    end_year = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum(Type, name='ExperienceType'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    location = db.Column(db.String(255))

    #relationships
    contact = db.relationship('Contact')
    achievements = db.relationship('Achievement', back_populates='experience',
                                   cascade='all, delete, delete-orphan')
    resumes = db.relationship('ResumeItem', back_populates='experience',
                              cascade='all, delete, delete-orphan')
    skills = db.relationship('SkillItem', secondary=experience_skills,
                             order_by='SkillItem.name',
                             lazy='subquery')

    #calculated fields
    @hybrid_property
    def date_end(self):
        if self.end_month==Month.none or self.end_year==0:
            return dt.datetime.today()
        else:
            end_str = f'1 {self.end_month.value}, {self.end_year}'
            return dt.datetime.strptime(end_str, '%d %B, %Y')

    @hybrid_property
    def date_start(self):
         if self.start_month==Month.none or self.start_year==0:
            return dt.datetime.today()
         else:
            start_str = f'1 {self.start_month.value}, {self.start_year}'
            return dt.datetime.strptime(start_str, '%d %B, %Y')

    @hybrid_property
    def date_length(self):
        end = self.date_end
        start = self.date_start
        return (end.year - start.year) * 12 + end.month - start.month

    @hybrid_property
    def length_year(self):
        return math.floor(self.date_length/12)

    @hybrid_property
    def length_month(self):
        return self.date_length % 12

    @hybrid_property
    def is_current(self):
        if self.end_month==Month.none or self.end_year==0:
            return True
        else:
            return False


class ExperienceSchema(Schema):
    id = fields.Integer(dump_only=True)
    description = fields.String()
    host = fields.String(required=True)
    title = fields.String(required=True)
    degree = fields.String()
    degree_other = fields.String()
    link = fields.String()
    is_current = fields.Boolean(dump_only=True)
    start_month = EnumField(Month, by_value=True, required=True)
    start_year = fields.Integer(required=True)
    end_month = EnumField(Month, by_value=True, required=True)
    end_year = fields.Integer(required=True)
    length_year = fields.Integer(dump_only=True)
    length_month = fields.Integer(dump_only=True)
    type = EnumField(Type, by_value=True)
    contact_id = fields.Integer(required=True)
    location = fields.String()
    achievements = fields.Nested(AchievementSchema, many=True)
    skills = fields.Nested(SkillItemSchema, many=True)

    class Meta:
        unknown = EXCLUDE
