from models.base_model import db
from marshmallow import Schema, fields
from models.resume_section_model import ResumeSection, ResumeSectionSchema
from models.contact_model import ContactSchema


class Resume(db.Model):
    __tablename__ = 'resume'
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.Date, nullable=False)

    #relationships
    contact = db.relationship('Contact', back_populates='resumes')
    sections = db.relationship('ResumeSection', back_populates='resume',
                               cascade='all, delete, delete-orphan')

class ResumeSchema(Schema):
    id = fields.Integer(dump_only=True)
    contact_id = fields.Integer(required=True, load_only=True)
    contact = fields.Nested(ContactSchema, dump_only=True)
    name = fields.String(required=True)
    date_created = fields.Date(required=True)
    sections = fields.Nested(ResumeSectionSchema, dump_only=True, many=True,
                             exclude=['resume_id', 'contact_id'])
