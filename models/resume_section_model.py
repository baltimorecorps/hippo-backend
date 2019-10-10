from models.base_model import db
from models.resume_item_model import ResumeItem, ResumeItemSchema
from marshmallow import Schema, fields, EXCLUDE


class ResumeSection(db.Model):
    __tablename__ = 'resume_section'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    min_count = db.Column(db.Integer)
    max_count = db.Column(db.Integer)

    #relationships
    resume = db.relationship('Resume', back_populates='sections')
    items = db.relationship('ResumeItem', back_populates='section',
                            cascade='all, delete, delete-orphan')

class ResumeSectionSchema(Schema):
    id = fields.Integer(dump_only=True)
    contact_id = fields.Integer(load_only=True)
    resume_id = fields.Integer()
    name = fields.String()
    min_count = fields.Integer()
    max_count = fields.Integer()
    items = fields.Nested(ResumeItemSchema, many=True)

    class Meta:
        unknown = EXCLUDE
