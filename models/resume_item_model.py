from models.base_model import db
from models.tag_item_model import TagItem, TagItemSchema
from models.experience_model import Experience, ExperienceSchema
from models.achievement_model import Achievement, AchievementSchema
from marshmallow import Schema, fields

class ResumeItem(db.Model):
    __tablename__ = "resume_item"

    #table columns
    resume_order = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('resume_section.id'), nullable=False, primary_key=True)
    exp_id = db.Column(db.Integer, db.ForeignKey('experience.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag_item.id'))
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'))
    indented = db.Column(db.Boolean, default=False)

    #relationships
    section = db.relationship('ResumeSection', back_populates='items')
    experience = db.relationship('Experience')
    tag_item = db.relationship('TagItem')
    accomplishment = db.relationship('Achievement')

class ResumeItemSchema(Schema):
    resume_order = fields.Integer()
    section_id = fields.Integer()
    indented = fields.Boolean()
    experience = fields.Nested(ExperienceSchema)
    tag = fields.Nested(TagItemSchema)
    achievement = fields.Integer(AchievementSchema)
