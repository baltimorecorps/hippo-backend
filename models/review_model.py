from models.base_model import db
from marshmallow import Schema, fields, post_dump, EXCLUDE

class Review(db.Model):
    __tablename__='review'

    #table columns
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    score = db.Column(db.Integer)
    stage = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    card_id = db.Column(db.String(25))
    program_contact_id = db.Column(db.Integer,
                                   db.ForeignKey('program_contact.id'),
                                   nullable=False)

    #relationships
    program_contact = db.relationship('ProgramContact',
                                      back_populates='reviews')

    def update(self, **update_dict):
        for field, value in update_dict.items():
            setattr(self, field, value)
        db.session.commit()

class ReviewSchema(Schema):
    id = fields.Integer(dump_only=True)
    is_active = fields.Boolean()
    stage = fields.Integer()
    card_id = fields.String()
    score = fields.Integer()

    class Meta:
        unknown = EXCLUDE
