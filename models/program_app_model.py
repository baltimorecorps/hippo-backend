from models.base_model import db
from marshmallow import Schema, fields, EXCLUDE
from models.program_model import Program, ProgramSchema
from sqlalchemy.ext.hybrid import hybrid_property


class ProgramApp(db.Model):
    __tablename__ = 'program_app'

    #table columns
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_interested = db.Column(db.Boolean, default=False)
    decision_date = db.Column(db.Date)

    #relationship fields
    program = db.relationship('Program', back_populates='program_apps')
    contact = db.relationship('Contact', back_populates='program_apps')

    # for more info on why to use setattr() read this:
    # https://medium.com/@s.azad4/modifying-python-objects-within-the-sqlalchemy-framework-7b6c8dd71ab3
    def update(self, **update_dict):
        for field, value in update_dict.items():
            if field in UPDATE_FIELDS:
                setattr(self, field, value)

    @hybrid_property
    def status(self):
        if not self.is_interested:
            return 'Not interested'
        elif self.is_interested and self.is_approved:
            return 'Eligible'
        else:
            return 'Waiting for approval'

class ProgramAppSchema(Schema):
    id = fields.Integer()
    program = fields.Nested(ProgramSchema)
    status = fields.String(dump_only=True)
    is_approved = fields.Boolean(allow_none=True)
    is_interested = fields.Boolean(allow_none=True)
    decision_date = fields.Date(dump_only=True)

    class Meta:
        unknown = EXCLUDE

# isolates the fields that can be updated in a PUT request
UPDATE_FIELDS = ('is_approved', 'is_interested')
