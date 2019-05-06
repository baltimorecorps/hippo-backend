from models.base_model import db
from models.tag_item_model import TagItem, TagItemSchema
from models.experience_model import Experience, ExperienceSchema
from models.achievement_model import Achievement, AchievementSchema
from marshmallow import Schema, fields

class ResumeItem(db.Model):
    __tablename__ = 'resumeitem' #should be changed to resume_item
                                 #after updating init.sql script

    #table columns
    resume_order = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('resumesection.id'), nullable=False, primary_key=True)
    exp_id = db.Column(db.Integer, db.ForeignKey('experience.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag_item.id'))
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    indented = db.Column(db.Boolean, default=False)

    #relationships
    section = db.relationship('ResumeSection', back_populates='items')
    experience = db.relationship('Experience')
    tag_item = db.relationship('TagItem')
    achievement = db.relationship('Achievement')
    resume = db.relationship('Resume')

class ResumeItemSchema(Schema):
    resume_order = fields.Integer()
    section_id = fields.Integer()
    indented = fields.Boolean()
    experience = fields.Nested(ExperienceSchema,
                               exclude=['achievements', 'contact_id'])
    tag = fields.Nested(TagItemSchema, exclude=['contact_id'])
    achievement = fields.Integer(AchievementSchema, only=['id', 'description'])
