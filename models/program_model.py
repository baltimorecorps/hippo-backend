from models.base_model import db
from marshmallow import Schema, fields, post_dump, EXCLUDE
from models.question_model import Question, QuestionSchema
from models.cycle_model import Cycle, CycleSchema


class Program(db.Model):

    #table columns
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    #relationship fields
    questions = db.relationship('Question', back_populates='program')
    cycles = db.relationship('Cycle', back_populates='program',
                             cascade='all, delete, delete-orphan')
    current_cycle = db.relationship('Cycle', primaryjoin=db.and_((id == Cycle.program_id),
                                    (Cycle.is_active == True)),
                                    uselist=False)
    contacts = db.relationship('ProgramContact', back_populates='program',
                               cascade='all, delete, delete-orphan')

class ProgramSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    current_cycle = fields.Nested(CycleSchema)

    class Meta:
        unknown = EXCLUDE
