from models.base_model import db
from marshmallow import Schema, fields
# from models.resume_item_model import ResumeItem


class Achievement(db.Model):
    __tablename__ = "achievement"
    id = db.Column(db.Integer, primary_key=True)
    exp_id = db.Column(db.Integer, db.ForeignKey("experience.id"))
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    description = db.Column(db.String(500))
    achievement_order = db.Column(db.Integer)
    # resumes = db.relationship("ResumeItem",
    #                           primaryjoin=(id == ResumeItem.achievement_id),
    #                           back_populates='achievement')
    experience = db.relationship('Experience')
    contact = db.relationship('Contact')


class AchievementSchema(Schema):
    id = fields.Integer()
    exp_id = fields.Integer()
    contact_id = fields.Integer()
    description = fields.String()
    achievement_order = fields.Integer()
