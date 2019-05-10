from models.base_model import db
from marshmallow import Schema, fields


class Achievement(db.Model):
    __tablename__ = 'achievement'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    exp_id = db.Column(db.Integer, db.ForeignKey('experience.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    description = db.Column(db.String(500))

    #relationships
    experience = db.relationship('Experience', back_populates='achievements')
    contact = db.relationship('Contact', back_populates='achievements')
    resumes = db.relationship('ResumeItem', back_populates='achievement',
                              cascade='all, delete, delete-orphan')


class AchievementSchema(Schema):
    id = fields.Integer(dump_only=True)
    description = fields.String()
