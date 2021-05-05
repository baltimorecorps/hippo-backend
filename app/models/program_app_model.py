from sqlalchemy.ext.hybrid import hybrid_property

from app.models import db, Program

# isolates the fields that can be updated in a PUT request
UPDATE_FIELDS = ('is_approved', 'is_interested')


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

    # for more info on why we use setattr() read this:
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
