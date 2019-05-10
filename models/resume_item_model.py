from models.base_model import db
from models.tag_item_model import TagItem, TagItemSchema
from models.experience_model import Experience, ExperienceSchema
from models.achievement_model import Achievement, AchievementSchema
from marshmallow import Schema, fields

class ResumeItem(db.Model):
    __tablename__ = 'resume_item'

    #table columns
    resume_order = db.Column(db.Integer, nullable=False, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('resume_section.id'),
                           nullable=False, primary_key=True)
    exp_id = db.Column(db.Integer, db.ForeignKey('experience.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag_item.id'))
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    indented = db.Column(db.Boolean, default=False)

    #relationships
    section = db.relationship('ResumeSection', back_populates='items')
    experience = db.relationship('Experience')
    tag = db.relationship('TagItem')
    achievement = db.relationship('Achievement')
    resume = db.relationship('Resume')

class ResumeItemSchema(Schema):
    resume_order = fields.Integer(required=True)
    indented = fields.Boolean()
    exp_id = fields.Integer(load_only=True)
    tag_id = fields.Integer(load_only=True)
    achievement_id = fields.Integer(load_only=True)
    experience = fields.Nested(ExperienceSchema, dump_only=True,
                               exclude=['achievements', 'contact_id'])
    tag = fields.Nested(TagItemSchema, dump_only=True, exclude=['contact_id'])
    achievement = fields.Integer(AchievementSchema, dump_only=True)
