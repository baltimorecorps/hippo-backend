# TODO: DELETE THIS

import json
from models.base_model import db
from marshmallow import Schema, fields, EXCLUDE, pre_load, post_dump
from models.resume_section_model import ResumeSection, ResumeSectionSchema
from models.contact_model import ContactSchema
from models.experience_model import ExperienceSchema
from models.tag_item_model import TagItemSchema


class Resume(db.Model):
    __tablename__ = 'resume'
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    gdoc_id = db.Column(db.String(255))

    #relationships
    #contact = db.relationship('Contact', back_populates='resumes')
    #sections = db.relationship('ResumeSection', back_populates='resume',
    #                           cascade='all, delete, delete-orphan')

class ResumeSnapshot(db.Model):
    __tablename__ = 'resume_snapshot'
    id = db.Column(db.Integer, primary_key=True)
    resume = db.Column(db.Text, nullable=False)

class ResumeSchemaNew(Schema):
    #fields used to load the data from the POST request
    name = fields.String(required=True)
    relevant_exp = fields.List(fields.Integer(), load_only=True)
    other_exp = fields.List(fields.Integer(), load_only=True)
    relevant_edu = fields.List(fields.Integer(), load_only=True)
    other_edu = fields.List(fields.Integer(), load_only=True)
    relevant_achieve = fields.List(fields.Integer(), load_only=True)
    other_achieve = fields.List(fields.Integer(), load_only=True)
    relevant_skills = fields.List(fields.Integer(), load_only=True)
    other_skills = fields.List(fields.Integer(), load_only=True)

    #fields used to dump the data from the post request
    id = fields.Integer(dump_only=True)
    contact = fields.Nested(ContactSchema, dump_only=True)
    gdoc_id = fields.String(dump_only=True)
    date_created = fields.Date(required=True, dump_only=True)
    relevant_exp_dump = fields.Nested(ExperienceSchema, many=True, dump_only=True)
    other_exp_dump = fields.Nested(ExperienceSchema, many=True, dump_only=True)
    relevant_edu_dump = fields.Nested(ExperienceSchema, many=True, dump_only=True)
    other_edu_dump = fields.Nested(ExperienceSchema, many=True, dump_only=True)
    relevant_achieve_dump = fields.Nested(ExperienceSchema, many=True, dump_only=True)
    other_achieve_dump = fields.Nested(ExperienceSchema, many=True, dump_only=True)
    relevant_skills_dump = fields.Nested(TagItemSchema, many=True, dump_only=True)
    other_skills_dump = fields.Nested(TagItemSchema, many=True, dump_only=True)

    class Meta:
        unknown = EXCLUDE

class ResumeSchema(Schema):
    id = fields.Integer(dump_only=True)
    contact_id = fields.Integer(required=True, load_only=True)
    contact = fields.Nested(ContactSchema, dump_only=True)
    name = fields.String(required=True)
    date_created = fields.Date(required=True)
    gdoc_id = fields.String(dump_only=True)
    #sections = fields.Nested(ResumeSectionSchema, dump_only=True, many=True,
    #                         exclude=['resume_id', 'contact_id'])

class ResumeSnapshotSchema(Schema):
    resume = fields.String(required=True)

    @pre_load(pass_many=False)
    def pack_json(self, data, many, **kwargs):
        if 'resume' in data:
            data['resume'] = json.dumps(data['resume'], separators=(',',':'))
        return data

    @post_dump(pass_many=False)
    def unpack_json(self, data, many, **kwargs):
        if 'resume' in data:
            data['resume'] = json.loads(data['resume'])
        return data
