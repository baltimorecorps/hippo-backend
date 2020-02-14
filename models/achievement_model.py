from models.base_model import db
from models.skill_model import SkillSchema
from models.skill_item_model import AchievementSkill
from marshmallow import Schema, fields, EXCLUDE
from sqlalchemy.ext.associationproxy import association_proxy

def add_skill_error(_):
    assert False, "use experience.add_skill instead of experience.skills.append"

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
    skill_items = db.relationship('AchievementSkill', 
                           cascade='all, delete, delete-orphan')
    skills = association_proxy('skill_items', 'skill', creator=add_skill_error )

    def add_skill(self, skill):
        experience_skill = self.experience.add_skill(skill)
        if skill in self.skills:
            return (AchievementSkill.query
                                   .filter_by(achievement_id=self.id,
                                              parent_id=contact_skill.id)
                                   .first())
        else:
            achievement_skill = AchievementSkill(experience_skill, self)
            self.skill_items.append(achievement_skill)
            return achievement_skill


class AchievementSchema(Schema):
    id = fields.Integer(dump_only=True)
    description = fields.String()
    skills = fields.Nested(SkillSchema, many=True)

    class Meta:
        unknown = EXCLUDE
