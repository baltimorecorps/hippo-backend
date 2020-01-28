from models.base_model import db
from marshmallow import Schema, fields, post_dump, EXCLUDE

class Review(db.Model):

    #table columns
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    reviewer = db.Column(db.String(50))
    score = db.Column(db.Integer)
    stage = db.Column(db.Integer)
    card_id = db.Column(db.String(25))
    program_contact_id = db.Column(db.Integer,
                                   db.ForeignKey('program_contact.id'),
                                   nullable=False)
