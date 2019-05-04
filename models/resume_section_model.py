from models.base_model import db
from models.resume_item_model import ResumeItem, ResumeItemSchema
from marshmallow import Schema, fields


class ResumeSection(db.Model):
    __tablename__ = 'resume_section'
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    min_count = db.Column(db.Integer)
    max_count = db.Column(db.Integer)

    #relationships
    resume = db.relationship('Resume', back_populates='sections')
    items = db.relationship('ResumeItem', back_populates='section')

class ResumeSectionSchema(Schema):
    id = fields.Integer()
    resume_id = fields.Integer()
    name = fields.String()
    min_count = fields.Integer()
    max_count = fields.Integer()
    items = fields.Nested(ResumeItemSchema, many=True)
