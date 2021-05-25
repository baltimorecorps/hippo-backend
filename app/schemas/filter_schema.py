from marshmallow_enum import EnumField
from marshmallow import Schema, fields, EXCLUDE, ValidationError

from app.models import ContactStage
from app.schemas import (
    ProgramAppSchema,
    RoleChoiceSchema,
    ProgramsCompletedSchema,
)


class FilterInputSchema(Schema):
    status = fields.List(fields.String(),allow_none=True)
    years_exp = fields.List(fields.String(), allow_none=True)
    job_search_status = fields.List(fields.String(), allow_none=True)
    current_job_status = fields.List(fields.String(), allow_none=True)
    current_edu_status = fields.List(fields.String(), allow_none=True)
    previous_bcorps_program = fields.List(fields.String(), allow_none=True)
    skills = fields.List(fields.String(), allow_none=True)
    hear_about_us = fields.List(fields.String(), allow_none=True)
    roles = fields.Nested(RoleChoiceSchema, allow_none=True)
    programs_completed = fields.Nested(ProgramsCompletedSchema, allow_none=True)
    program_apps = fields.Nested(ProgramAppSchema,
                                 many=True,
                                 allow_none=True)

    class Meta:
        unknown = EXCLUDE
