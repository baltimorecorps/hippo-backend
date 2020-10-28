
import enum
from marshmallow import Schema, fields, EXCLUDE, pre_dump, post_dump
from marshmallow_enum import EnumField
from sqlalchemy.ext.hybrid import hybrid_property

from models.base_model import db
from models.experience_model import Experience, ExperienceSchema, Type
from models.email_model import Email, EmailSchema
from models.achievement_model import Achievement
from models.skill_model import Skill, SkillSchema
from models.skill_item_model import ContactSkill
from models.program_app_model import ProgramAppSchema, ProgramApp
from models.profile_model import ProfileSchema, ContactAddress

UPDATE_FIELDS = [
    'first_name', 'last_name', 'email', 'phone_primary', 'stage', 'card_id'
]

def add_skill_error(_):
    assert False, "use contact.add_skill instead of contact.skills.append"

class ContactStage(enum.Enum):
    created = 1
    submitted = 2
    approved = 3

class Contact(db.Model):
    __tablename__ = 'contact'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String)
    phone_primary = db.Column(db.String(25))
    account_id = db.Column(db.String(255), nullable=True)
    terms_agreement =db.Column(db.Boolean, default=False)
    stage = db.Column(db.Integer, default=1)
    card_id = db.Column(db.String)

    #relationships
    emails = db.relationship('Email',
                             back_populates='contact',
                             cascade='all, delete, delete-orphan')
    email_primary = db.relationship("Email",
                                    primaryjoin=db.and_(
                                    id == Email.contact_id,
                                    Email.is_primary == True),
                                    uselist=False)
    addresses = db.relationship('ContactAddress',
                                back_populates='contact')
    address_primary = db.relationship('ContactAddress',
                                      primaryjoin=db.and_(
                                      id == ContactAddress.contact_id,
                                      ContactAddress.is_primary == True),
                                      back_populates='contact',
                                      uselist=False)
    achievements = db.relationship('Achievement',
                                   back_populates='contact',
                                   cascade='all, delete, delete-orphan')
    skill_items = db.relationship('ContactSkill',
                                  cascade='all, delete, delete-orphan')
    capability_skill_suggestions = db.relationship(
        'CapabilitySkillSuggestion',
        cascade='all, delete, delete-orphan'
    )
    experiences = db.relationship('Experience',
                                  back_populates='contact',
                                  cascade='all, delete, delete-orphan')
    program_apps = db.relationship('ProgramApp',
                                   back_populates='contact',
                                   cascade='all, delete, delete-orphan')
    programs_interested = db.relationship('ProgramApp',
                                          primaryjoin=db.and_(
                                          id == ProgramApp.contact_id,
                                          ProgramApp.is_interested),
                                          back_populates='contact')
    applications = db.relationship('OpportunityApp',
                                   back_populates='contact',
                                   cascade='all, delete, delete-orphan')
    sessions = db.relationship('UserSession',
                               cascade='all, delete, delete-orphan')
    profile = db.relationship('Profile',
                              back_populates='contact',
                              uselist=False,
                              cascade='all, delete, delete-orphan')
    race = db.relationship('Race',
                           back_populates='contact',
                           cascade='all, delete, delete-orphan',
                           uselist=False)

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
    def email_main(self):
        if not self.email:
            return self.email_primary.email
        else:
            return self.email

    @hybrid_property
    def tag_skills_complete(self):
        return (len(self.skills) >= 3)

    @hybrid_property
    def add_experience_complete(self):
        complete_experience = [exp for exp in self.experiences
                               if exp.type == Type('Work')
                               and exp.tag_skills_complete
                               and exp.add_achievements_complete]
        status = (len(complete_experience) >= 1)
        exp_dict = {
            'is_complete': status,
            'components': {
                'tag_skills': status,
                'add_achievements': status
            }
        }
        return exp_dict

    @hybrid_property
    def add_education_complete(self):
        complete_education = [exp for exp in self.experiences
                              if exp.type == Type('Education')]
        return (len(complete_education) >= 1)

    @hybrid_property
    def add_portfolio_complete(self):
        complete_portfolio = [exp for exp in self.experiences
                             if exp.type == Type('Accomplishment')]
        return (len(complete_portfolio) >= 1)

    @hybrid_property
    def profile_complete(self):
        profile_status = (self.add_experience_complete['is_complete']
                          and self.add_education_complete)
        profile_dict = {
            'is_complete': profile_status,
            'components': {
                'tag_skills': self.tag_skills_complete,
                'add_experience': self.add_experience_complete,
                'add_education': self.add_education_complete,
                'add_portfolio': self.add_portfolio_complete,
            }
        }
        return profile_dict

    @hybrid_property
    def about_me_complete(self):
        if self.profile:
            about_me_status = (
                self.profile.candidate_info_complete
                and self.profile.value_alignment_complete
                and self.profile.interests_and_goals_complete
                and self.profile.programs_and_eligibility_complete
            )
            about_me_dict = {
                'is_complete': about_me_status,
                'components': {
                    'candidate_information': self.profile.candidate_info_complete,
                    'value_alignment': self.profile.value_alignment_complete,
                    'programs': self.profile.programs_and_eligibility_complete,
                    'interests': self.profile.interests_and_goals_complete,
                }
            }
        else:
            about_me_dict = {
                'is_complete': False,
                'components': {
                    'candidate_information': False,
                    'value_alignment': False,
                    'programs': False,
                    'interests': False,
                }
            }
        return about_me_dict

    @hybrid_property
    def submit_complete(self):
        return {'is_complete': self.stage >= 2}

    @hybrid_property
    def status(self):
        return ContactStage(self.stage)

    @hybrid_property
    def race_list(self):
        race_dict = {
            'american_indian': 'American Indian or Alaskan Native',
            'asian':'Asian',
            'black': 'Black or African Descent',
            'hawaiian': 'Native Hawaiian or Other Pacific Islander',
            'hispanic': 'Hispanic or Latinx',
            'south_asian': 'South Asian',
            'white': 'White',
            'not_listed': 'Not Listed',
        }
        race_list = [race_dict[r] for r in race_dict.keys()
                     if self.race.getattr(r)]
        return race_list

    @hybrid_property
    def instructions(self):
        instructions_dict = {
            'profile': self.profile_complete,
            'about_me': self.about_me_complete,
            'submit': self.submit_complete
        }
        return instructions_dict

    def query_program_contact(self, program_id):
        return next((p for p in self.programs
                     if p.program_id == program_id), None)

    def update(self, **update_dict):
        for field, value in update_dict.items():
            if field in UPDATE_FIELDS:
                setattr(self, field, value)

class ContactSchema(Schema):
    # Short contact
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(load_only=True)
    email_main = fields.String(dump_only=True, data_key='email')
    phone_primary = fields.String()
    account_id = fields.String()
    status = EnumField(ContactStage, dump_only=True)
    terms_agreement = fields.Boolean(load_only=True)

    # TODO: Remove this when Frontend switches
    email_primary = fields.Nested(EmailSchema)

    # Full contact
    skills = fields.Nested(SkillSchema, many=True)
    program_apps = fields.Nested(ProgramAppSchema,
                                 exclude=['program_name'],
                                 many=True)
    profile = fields.Nested(ProfileSchema)
    instructions = fields.Dict()
    experiences = fields.Nested(ExperienceSchema, many=True, dump_only=True)

    class Meta:
        unknown = EXCLUDE

class ContactShortSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    email_main = fields.String(dump_only=True, data_key='email')
    phone_primary = fields.String()
    account_id = fields.String()
    status = EnumField(ContactStage, dump_only=True)

    class Meta:
        unknown = EXCLUDE
