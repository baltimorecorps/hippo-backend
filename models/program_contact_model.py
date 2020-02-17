from models.base_model import db
from marshmallow import Schema, fields, EXCLUDE
from models.program_model import Program, ProgramSchema
from models.response_model import Response, ResponseSchema
from models.review_model import Review, ReviewSchema


class ProgramContact(db.Model):
    __tablename__ = 'program_contact'

    #table columns
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    card_id = db.Column(db.String(25))
    stage = db.Column(db.Integer)
    is_approved = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    #relationship fields
    program = db.relationship('Program', back_populates='contacts')
    contact = db.relationship('Contact', back_populates='programs')
    responses = db.relationship('Response',
                                back_populates='program_contact',
                                cascade='all, delete, delete-orphan')
    reviews = db.relationship('Review',
                              back_populates='program_contact',
                              cascade='all, delete, delete-orphan')

    # for more info on why to use setattr() read this:
    # https://medium.com/@s.azad4/modifying-python-objects-within-the-sqlalchemy-framework-7b6c8dd71ab3
    def update(self, **update_dict):
        for field, value in update_dict.items():
            setattr(self, field, value)
        db.session.commit()

class ProgramContactSchema(Schema):
    id = fields.Integer(dump_only=True)
    contact_id = fields.Integer()
    program_id = fields.Integer(load_only=True)
    program = fields.Nested(ProgramSchema, dump_only=True)
    responses = fields.Nested(ResponseSchema, many=True)
    card_id = fields.String()
    stage = fields.Integer()
    is_approved = fields.Boolean()
    is_active = fields.Boolean()
    reviews = fields.Nested(ReviewSchema, many=True, dump_only=True,
                            cascade='all, delete, delete-orphan')

    class Meta:
        unknown = EXCLUDE

# isolates the fields that can be updated in a PUT request
UPDATE_FIELDS = ('card_id', 'is_approved', 'is_active', 'stage')
