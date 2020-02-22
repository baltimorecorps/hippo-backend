from models.base_model import db
from models.contact_model import ContactSchema
from models.opportunity_app_model import ApplicationStage
from marshmallow import Schema, fields, EXCLUDE
from marshmallow_enum import EnumField
from sqlalchemy.ext.hybrid import hybrid_property
import enum

class OpportunityStage(enum.Enum):
    started = 0
    submitted = 1
    approved = 2
    posted = 3
    interviewing = 4
    filled = 5

class Opportunity(db.Model):
    __tablename__ = 'opportunity'

    #table columns
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.String(2000), nullable=False)
    gdoc_id = db.Column(db.String(200), nullable=False)
    card_id = db.Column(db.String, nullable=False)
    stage = db.Column(db.Integer, default=1)

    applications = db.relationship('OpportunityApp', back_populates='opportunity',
                                   cascade='all, delete, delete-orphan')

    @hybrid_property
    def status(self):
        return OpportunityStage(self.stage)

class OpportunityAppSchema(Schema):
    id = fields.String(dump_only=True)
    contact = fields.Nested(ContactSchema, dump_only=True)
    # for info on why we use lambda here review this documentation:
    # https://marshmallow.readthedocs.io/en/stable/nesting.html#two-way-nesting
    opportunity = fields.Nested(lambda: OpportunitySchema(exclude=('applications',)))
    interest_statement = fields.String()
    status = EnumField(ApplicationStage, dump_only=True)

    class Meta:
        unknown = EXCLUDE

class OpportunitySchema(Schema):
    id = fields.String(required=True, dump_only=True)
    title = fields.String(required=True)
    short_description = fields.String(required=True)
    gdoc_id = fields.String(required=True)
    status = EnumField(OpportunityStage, dump_only=True)
    applications = fields.Nested(OpportunityAppSchema(exclude=('opportunity',), many=True))

    class Meta:
        unknown = EXCLUDE
