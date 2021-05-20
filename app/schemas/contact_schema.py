from marshmallow import Schema, fields, EXCLUDE, pre_dump, post_dump
from marshmallow_enum import EnumField

from app.schemas import (
    EmailSchema,
    ExperienceSchema,
    ProfileSchema,
    ProgramAppSchema,
    SkillSchema,
)
from app.models import ContactStage


class ContactSchema(Schema):
    # Short contact
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(load_only=True)
    email_main = fields.String(dump_only=True, data_key='email')
    phone_primary = fields.String()
    account_id = fields.String()
    status = EnumField(ContactStage, dump_only=True)
    terms_agreement = fields.Boolean(load_only=True)

    # TODO: Remove this when Frontend switches
    email_primary = fields.Nested(EmailSchema)

    # Full contact
    skills = fields.Nested(SkillSchema, many=True)
    program_apps = fields.Nested(ProgramAppSchema,
                                 exclude=['program_name'],
                                 many=True)
    profile = fields.Nested(ProfileSchema)
    instructions = fields.Dict()
    experiences = fields.Nested(ExperienceSchema, many=True, dump_only=True)

    class Meta:
        unknown = EXCLUDE

class ContactShortSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    email_main = fields.String(dump_only=True, data_key='email')
    phone_primary = fields.String()
    account_id = fields.String()
    status = EnumField(ContactStage, dump_only=True)

    class Meta:
        unknown = EXCLUDE
