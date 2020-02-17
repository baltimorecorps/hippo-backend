from models.base_model import db
from marshmallow import Schema, fields, EXCLUDE

class Opportunity(db.Model):
    __tablename__ = 'opportunity'

    #table columns
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.String(2000), nullable=False)
    gdoc_id = db.Column(db.String(200), nullable=False)

    applications = db.relationship('OpportunityApp', back_populates='opportunity',
                                   cascade='all, delete, delete-orphan')


class OpportunitySchema(Schema):
    id = fields.String(required=True, dump_only=True)
    title = fields.String(required=True)
    short_description = fields.String(required=True)
    gdoc_id = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE



