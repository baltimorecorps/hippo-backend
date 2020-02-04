from models.base_model import db
from marshmallow import Schema, fields, post_dump, EXCLUDE


class Question(db.Model):

    #table columns
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    limit_word = db.Column(db.Integer)
    limit_character = db.Column(db.Integer)

    #relationship fields
    program = db.relationship('Program', back_populates='questions')

class QuestionSchema(Schema):
    id = fields.Integer(dump_only=True)
    program_id = fields.Integer(required=True)
    question_text = fields.String(required=True)
    limit_word = fields.Integer()
    limit_character = fields.Integer()

    class Meta:
        unknown = EXCLUDE
