from models.base_model import db
from marshmallow import Schema, fields, post_dump, EXCLUDE
from sqlalchemy.ext.associationproxy import association_proxy

# We make heavy use of this to create a tree structure for skill associations
# https://docs.sqlalchemy.org/en/13/orm/extensions/associationproxy.html
class ContactSkill(db.Model):
    __tablename__ = 'skill_item'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.String, db.ForeignKey('skill.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)

    #relationships
    skill = db.relationship('Skill')
    experiences = db.relationship('ExperienceSkill', 
                                  back_populates='parent',
                                  cascade='all, delete, delete-orphan')
    contact = db.relationship('Contact', back_populates='skill_items')

    def __init__(self, skill=None, contact=None):
        self.skill = skill
        self.contact = contact


class ExperienceSkill(db.Model):
    __tablename__ = 'skill_item_experience'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('skill_item.id'))
    experience_id = db.Column(db.Integer, db.ForeignKey('experience.id'))

    #relationships
    parent = db.relationship('ContactSkill', back_populates='experiences')
    achievements = db.relationship('AchievementSkill', 
                                   back_populates='parent',
                                   cascade='all, delete, delete-orphan')

    skill = association_proxy('parent', 'skill')
    experience = db.relationship('Experience', back_populates='skill_items')

    def __init__(self, parent=None, experience=None):
        self.parent = parent
        self.experience = experience

class AchievementSkill(db.Model):
    __tablename__ = 'skill_item_achievement'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('skill_item_experience.id'))
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'))

    #relationships
    parent = db.relationship('ExperienceSkill', back_populates='achievements')
    skill = association_proxy('parent', 'skill')
    achievement = db.relationship('Achievement', back_populates='skill_items')

    def __init__(self, parent=None, achievement=None):
        self.parent = parent
        self.achievement = achievement

