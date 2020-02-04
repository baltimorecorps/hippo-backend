from models.base_model import db
from marshmallow import Schema, fields, post_dump, EXCLUDE


class Response(db.Model):

    #table columns
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    program_contact_id = db.Column(db.Integer, db.ForeignKey('program_contact.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    response_text = db.Column(db.String())

    #relationship fields
    program_contact = db.relationship('ProgramContact',
                                      back_populates='responses')

class ResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    program_contact_id = fields.Integer(required=True)
    question_id = fields.Integer(required=True)
    response_text = fields.String()

    class Meta:
        unknown = EXCLUDE
