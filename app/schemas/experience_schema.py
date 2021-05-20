from marshmallow import Schema, fields, EXCLUDE
from marshmallow_enum import EnumField

from app.schemas import AchievementSchema, SkillSchema
from app.models import Month, ExpType


class ExperienceSchema(Schema):
    id = fields.Integer(dump_only=True)
    description = fields.String(allow_none=True)
    host = fields.String(required=True)
    title = fields.String(required=True)
    degree = fields.String(allow_none=True)
    degree_other = fields.String(allow_none=True)
    link = fields.String(allow_none=True)
    link_name = fields.String(allow_none=True)
    is_current = fields.Boolean(dump_only=True)
    start_month = EnumField(Month, by_value=True, required=True)
    start_year = fields.Integer(required=True)
    end_month = EnumField(Month, by_value=True, required=True)
    end_year = fields.Integer(required=True)
    length_year = fields.Integer(dump_only=True)
    length_month = fields.Integer(dump_only=True)
    type = EnumField(ExpType, by_value=True)
    contact_id = fields.Integer(required=True)
    location = fields.String(allow_none=True)
    achievements = fields.Nested(AchievementSchema, many=True)
    skills = fields.Nested(SkillSchema, many=True)

    class Meta:
        unknown = EXCLUDE
