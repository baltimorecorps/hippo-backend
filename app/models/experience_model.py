import math
import enum
import datetime as dt

from sqlalchemy.ext.hybrid import hybrid_property

from app.models import db, Achievement, ExperienceSkill


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


def add_skill_error(_):
    assert False, "use experience.add_skill instead of experience.skills.append"


class Experience(db.Model):
    __tablename__ = 'experience'

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    host = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    degree_other = db.Column(db.String(100))
    degree = db.Column(db.String(100))
    link = db.Column(db.String)
    link_name = db.Column(db.String)
    start_month = db.Column(db.Enum(Month, name='MonthType'), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_month = db.Column(db.Enum(Month, name='MonthType'), nullable=False)
    end_year = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum(Type, name='ExperienceType'))
    contact_id = db.Column(db.Integer, db.ForeignKey(
        'contact.id'), nullable=False)
    location = db.Column(db.String(255))

    # relationships
    contact = db.relationship('Contact')
    achievements = db.relationship('Achievement', back_populates='experience',
                                   cascade='all, delete, delete-orphan')

    skill_items = db.relationship('ExperienceSkill',
                                  cascade='all, delete, delete-orphan')

    def add_skill(self, skill):
        contact_skill = self.contact.add_skill(skill)
        exp_skill = (ExperienceSkill.query
                     .filter_by(experience_id=self.id,
                                parent_id=contact_skill.id)
                     .first())
        if not exp_skill:
            exp_skill = ExperienceSkill(contact_skill, self)
            self.skill_items.append(exp_skill)
        return exp_skill

    # calculated fields
    @hybrid_property
    def skills(self):
        skills = [skill_item.skill for skill_item in self.skill_items
                  if not skill_item.deleted]
        return sorted(skills, key=lambda skill: skill.name)

    @hybrid_property
    def date_end(self):
        if self.end_month == Month.none or self.end_year == 0:
            return dt.datetime.today()
        else:
            end_str = f'1 {self.end_month.value}, {self.end_year}'
            return dt.datetime.strptime(end_str, '%d %B, %Y')

    @hybrid_property
    def date_start(self):
        if self.start_month == Month.none or self.start_year == 0:
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
        if self.end_month == Month.none or self.end_year == 0:
            return True
        else:
            return False

    @hybrid_property
    def tag_skills_complete(self):
        return len(self.skills) >= 1

    @hybrid_property
    def add_achievements_complete(self):
        return len(self.achievements) >= 2
