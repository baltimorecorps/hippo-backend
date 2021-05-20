from marshmallow import Schema, fields, EXCLUDE
from marshmallow_enum import EnumField

from app.schemas import ContactShortSchema, ResumeSnapshotSchema
from app.models import ApplicationStage, OpportunityStage


class OpportunityAppSchema(Schema):
    id = fields.String(dump_only=True)
    contact = fields.Nested(ContactShortSchema, dump_only=True)
    # for info on why we use lambda here review this documentation:
    # https://marshmallow.readthedocs.io/en/stable/nesting.html#two-way-nesting
    opportunity = fields.Nested(
        lambda: OpportunitySchema(exclude=('applications',)))
    interest_statement = fields.String()
    status = EnumField(ApplicationStage, dump_only=True)
    is_active = fields.Boolean(dump_only=True)
    resume = fields.Pluck(ResumeSnapshotSchema,
                          field_name='resume', allow_none=True)
    interview_date = fields.Date(allow_none=True)
    interview_time = fields.String(allow_none=True)
    interview_completed = fields.Boolean(dump_only=True)

    class Meta:
        unknown = EXCLUDE


class OpportunitySchema(Schema):
    id = fields.String(required=True, dump_only=True)
    title = fields.String(required=True)
    short_description = fields.String(required=True)
    gdoc_link = fields.String(required=True)
    status = EnumField(OpportunityStage, dump_only=True)
    org_name = fields.String(required=True)
    program_name = fields.String(allow_none=True)
    program_id = fields.Integer(allow_none=True)
    is_active = fields.Boolean(dump_only=True)
    applications = fields.Nested(OpportunityAppSchema(
        exclude=('opportunity', 'resume'), many=True))

    class Meta:
        unknown = EXCLUDE
