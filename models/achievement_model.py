from models.base_model import db
from models.skill_model import SkillSchema
from models.skill_item_model import AchievementSkill
from marshmallow import Schema, fields, EXCLUDE
from sqlalchemy.ext.hybrid import hybrid_property

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

    def add_skill(self, skill, capability=None):
        capability_id = capability.id if capability else None
        experience_skill = self.experience.add_skill(skill)
        achievement_skill = (AchievementSkill.query
                                   .filter_by(achievement_id=self.id,
                                              parent_id=experience_skill.id,
                                              capability_id=capability_id
                                              )
                                   .first())
        if not achievement_skill:
            achievement_skill = AchievementSkill(experience_skill, self, capability)
            self.skill_items.append(achievement_skill)
        return achievement_skill

    #calculated fields
    @hybrid_property
    def skills(self):
        skills = []
        for skill_item in self.skill_items:
            if not skill_item.deleted:
                skills.append({
                    'name': skill_item.skill.name,
                    'capability_id': skill_item.capability_id,
                })
        return sorted(skills, key=lambda skill: skill['name'])

class AchievementSkillItemSchema(Schema):
    name = fields.String(required=True)
    capability_id = fields.String(required=False, missing=None)

    class Meta:
        unknown = EXCLUDE

class AchievementSchema(Schema):
    id = fields.Integer(required=False)
    description = fields.String()
    skills = fields.Nested(AchievementSkillItemSchema, many=True)

    class Meta:
        unknown = EXCLUDE
