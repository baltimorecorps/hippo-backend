from models.base_model import db
from marshmallow import Schema, fields, post_dump, EXCLUDE


class Program(db.Model):

    #table columns
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    trello_board_id = db.Column(db.String)

    #relationship fields
    contacts = db.relationship('ProgramContact',
                               back_populates='program',
                               cascade='all, delete, delete-orphan')
    opportunities = db.relationship('Opportunity',
                               back_populates='program',
                               cascade='all, delete, delete-orphan')

class ProgramSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    trello_board_id = fields.String(dump_only=True)

    class Meta:
        unknown = EXCLUDE
