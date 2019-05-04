from models.base_model import db
from marshmallow import Schema, fields
from models.resume_section_model import ResumeSection


class Resume(db.Model):
    __tablename__ = "resume"
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    contact = db.relationship('Contact')

    #relationships
    sections = db.relationship('ResumeSection', back_populates='resume')


class ResumeSchema(Schema):
	id = fields.Integer()
	contact_id = fields.Integer(required=True)
	name = fields.String(required=True)
	date_created = fields.Date(required=True)
