from models.base_model import db
from marshmallow import Schema, fields, EXCLUDE
from models.contact_model import ContactSchema
from models.opportunity_model import OpportunitySchema

class OpportunityApp(db.Model):
    __tablename__ = 'opportunity_app'

    #table columns
    id = db.Column(db.String, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    opportunity_id = db.Column(db.String, db.ForeignKey('opportunity.id'), nullable=False)
    interest_statement = db.Column(db.String(2000), nullable=True)
    stage = db.Column(db.Integer, nullable=False, default=0)

    contact = db.relationship('Contact', back_populates='applications')

    opportunity = db.relationship('Opportunity')

    __table_args__ = (
        db.Index('oppapp_contact_opportunity', 
                 'contact_id', 'opportunity_id', unique=True),
    )


class OpportunityAppSchema(Schema):
    id = fields.String(dump_only=True)
    contact_id = fields.Integer(required=True, load_only=True)
    contact = fields.Nested(ContactSchema, dump_only=True)
    opportunity_id = fields.Integer(required=True, load_only=True)
    opportunity = fields.Nested(OpportunitySchema, dump_only=True)
    interest_statement = fields.String()
    stage = fields.Integer()

    class Meta:
        unknown = EXCLUDE



