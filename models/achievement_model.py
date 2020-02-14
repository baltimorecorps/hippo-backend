from models.base_model import db
from models.skill_item_model import experience_skills, SkillItemSchema
from marshmallow import Schema, fields, EXCLUDE


class Achievement(db.Model):
    __tablename__ = 'achievement'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    exp_id = db.Column(db.Integer, db.ForeignKey('experience.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    description = db.Column(db.String(2000))

    #relationships
    experience = db.relationship('Experience', back_populates='achievements')
    contact = db.relationship('Contact', back_populates='achievements')

class AchievementSchema(Schema):
    id = fields.Integer(dump_only=True)
    description = fields.String()
    skills = fields.Nested(SkillItemSchema, many=True)

    class Meta:
        unknown = EXCLUDE
