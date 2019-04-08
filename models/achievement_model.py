from models.base_model import db
from marshmallow import Schema, fields


class Achievement(db.Model):
    __tablename__ = "achievement"
    id = db.Column(db.Integer, primary_key=True)
    exp_id = db.Column(db.Integer, db.ForeignKey("experience.id"), nullable=False)
    description = db.Column(db.String(500))
    achievement_order = db.Column(db.Integer)
    experience = db.relationship('Experience')


class AchievementSchema(Schema):
    id = fields.Integer()
    exp_id = fields.Integer()
    description = fields.String()
    achievement_order = fields.Integer()