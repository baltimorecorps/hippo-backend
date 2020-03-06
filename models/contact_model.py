from models.base_model import db
import enum
from marshmallow import Schema, fields, EXCLUDE, pre_dump, post_dump
from marshmallow_enum import EnumField
from models.experience_model import Experience, ExperienceSchema, Type
from models.email_model import Email, EmailSchema
from models.address_model import Address
from models.achievement_model import Achievement
from models.skill_model import Skill, SkillSchema
from models.skill_item_model import ContactSkill
from models.program_contact_model import ProgramContactSchema
from sqlalchemy.ext.hybrid import hybrid_property

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

def add_skill_error(_):
    assert False, "use contact.add_skill instead of contact.skills.append"

class Contact(db.Model):
    __tablename__ = 'contact'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    salutation = db.Column(db.Enum(Salutation, name='Salutation'))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_primary = db.Column(db.String(25))
    gender = db.Column(db.String(100))
    gender_other = db.Column(db.String(255))
    race_all = db.Column(db.String(255))
    race_other = db.Column(db.String(255))
    pronouns = db.Column(db.String(100))
    pronouns_other = db.Column(db.String(255))
    birthdate = db.Column(db.Date)
    account_id = db.Column(db.String(255), nullable=True)
    terms_agreement =db.Column(db.Boolean, default=False)

    #relationships
    emails = db.relationship('Email', back_populates='contact',
                             cascade='all, delete, delete-orphan')
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

    skill_items = db.relationship('ContactSkill', 
                           cascade='all, delete, delete-orphan')
    capability_skill_suggestions = db.relationship('CapabilitySkillSuggestion', 
                           cascade='all, delete, delete-orphan')

    experiences = db.relationship('Experience', back_populates='contact',
                                  cascade='all, delete, delete-orphan')
    programs = db.relationship('ProgramContact', back_populates='contact',
                               cascade='all, delete, delete-orphan')
    applications = db.relationship('OpportunityApp', back_populates='contact',
                               cascade='all, delete, delete-orphan')

    def add_skill(self, skill):
        contact_skill = (ContactSkill.query
                                .filter_by(contact_id=self.id,
                                           skill_id=skill.id)
                                .first())
        if contact_skill:
            contact_skill.deleted = False
        else:
            contact_skill = ContactSkill(skill, self)
            self.skill_items.append(contact_skill)
        return contact_skill

    @hybrid_property
    def skills(self):
        skills = []
        for skill_item in self.skill_items:
            if not skill_item.deleted:
                skills.append(skill_item.skill)
        return sorted(skills, key=lambda skill: skill.name)

    @hybrid_property
    def email(self):
        return self.email_primary.email

class ContactSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email_primary = fields.Nested(EmailSchema)
    emails = fields.Nested(EmailSchema, many=True)
    phone_primary = fields.String()
    gender = fields.String(allow_none=True)
    gender_other = fields.String()
    race_all = fields.String()
    race_other = fields.String()
    pronouns = fields.String()
    pronouns_other = fields.String()
    birthdate = fields.Date(allow_none=True)
    account_id = fields.String()
    skills = fields.Nested(SkillSchema, many=True)
    terms_agreement = fields.Boolean()
    programs = fields.Nested(ProgramContactSchema, many=True, dump_only=True)

    class Meta:
        unknown = EXCLUDE

class ContactShortSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.String(dump_only=True)
