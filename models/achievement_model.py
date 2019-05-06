from models.base_model import db
from marshmallow import Schema, fields


class Achievement(db.Model):
    __tablename__ = 'achievement'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    exp_id = db.Column(db.Integer, db.ForeignKey('experience.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    description = db.Column(db.String(500))

    #relationships
    experience = db.relationship('Experience', back_populates='achievements')
    contact = db.relationship('Contact', back_populates='achievements')
    resumes = db.relationship('ResumeItem', back_populates='achievement', 
                              cascade='all, delete, delete-orphan')


class AchievementSchema(Schema):
    id = fields.Integer()
    exp_id = fields.Integer()
    contact_id = fields.Integer()
    description = fields.String()
