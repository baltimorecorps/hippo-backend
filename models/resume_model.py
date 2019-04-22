from models.base_model import db
import enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from sqlalchemy_enum34 import EnumType
from models.achievement_model import Achievement, AchievementSchema

class ResumeTemplate(db.Model):
    __tablename__ = "resume_template"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    template_url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=False)

class Resume(db.Model):
    __tablename__ = "resume"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship('Contact')
    template_id = db.Column(db.Integer, db.ForeignKey("resume_template.id"), nullable=False)
    template = db.relationship('Template')

class ResumeExperience(db.Model):
    __tablename__ = "resume_experience"
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resume.id"), nullable=False)
    resume = db.relationship('Resume')
    exp_id = db.Column(db.Integer, db.ForeignKey("experience.id"), nullable=False)
    experience = db.relationship('Experience')
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date)
    score = db.Column(db.DECIMAL)
    resume_exp_order = db.Column(db.Integer, nullable=False)

class ResumeTag(db.Model):
    __tablename__ = "resume_tag"
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resume.id"), nullable=False)
    resume = db.relationship('Resume')
    tag_item_id = db.Column(db.Integer, db.ForeignKey("tag_item.id"), nullable=False)
    tagitem = db.relationship('TagItem')
    score = db.Column(db.DECIMAL)
    resume_tag_order = db.Column(db.Integer, nullable=False)

class ResumeAchievement(db.Model):
    __tablename__ = "resume_achievement"
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resume.id"), nullable=False)
    resume = db.relationship('Resume')
    resume_tag_id = db.Column(db.Integer, db.ForeignKey("resume_tag.id"), nullable=False)
    resume_tag = db.relationship('Resume Tag')
    resume_exp_id = db.Column(db.Integer, db.ForeignKey("resume_exp.id"), nullable=False)
    resume_exp = db.relationship('Resume Exp')
    achievement_id = db.Column(db.Integer, db.ForeignKey("achievement.id"), nullable=False)
    achievement = db.relationship('Achievement')
    score = db.Column(db.DECIMAL)
    resume_achievement_order = db.Column(db.Integer, nullable=False)




class ResumeTemplateSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    template_url = fields.String(required=True)
    description = fields.String(required=True)

class ResumeSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    date_created = fields.Date(required=True)
    contact_id = fields.Integer(required=True)
    template_id = fields.Integer(required=True)

class ResumeExperienceSchema(Schema):
    id = fields.Integer()
    resume_id = fields.String(required=True)
    exp_id = fields.String(required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date()
    score = fields.Decimal()
    resume_exp_order = fields.Integer(required=True)

class ResumeTagSchema(Schema):
    id = fields.Integer()
    resume_id = fields.String(required=True)
    tag_item_id = fields.String(required=True)
    score = fields.Decimal()
    resume_tag_order = fields.Integer(required=True)

class ResumeAchievementSchema(Schema):
    id = fields.Integer()
    resume_id = fields.String(required=True)
    resume_tag_id = fields.String(required=True)
    resume_exp_id = fields.String(required=True)
    achievement_id = fields.String(required=True)
    score = fields.Decimal()
    resume_achievement_order = fields.Integer(required=True)