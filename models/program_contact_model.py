from models.base_model import db
from marshmallow import Schema, fields, EXCLUDE
from models.program_model import Program, ProgramSchema
from sqlalchemy.ext.hybrid import hybrid_property


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

    # for more info on why to use setattr() read this:
    # https://medium.com/@s.azad4/modifying-python-objects-within-the-sqlalchemy-framework-7b6c8dd71ab3
    def update(self, **update_dict):
        for field, value in update_dict.items():
            if field in UPDATE_FIELDS:
                setattr(self, field, value)
        db.session.commit()

    @hybrid_property
    def applications(self):
        return [app for app in self.contact.applications
                if app.program_id == self.program_id]

class ProgramContactSchema(Schema):
    id = fields.Integer(dump_only=True)
    contact_id = fields.Integer()
    program_id = fields.Integer(load_only=True)
    program = fields.Nested(ProgramSchema, dump_only=True)
    card_id = fields.String()
    stage = fields.Integer()
    is_approved = fields.Boolean()
    is_active = fields.Boolean()

    class Meta:
        unknown = EXCLUDE

# isolates the fields that can be updated in a PUT request
UPDATE_FIELDS = ('card_id', 'is_approved', 'is_active', 'stage')
