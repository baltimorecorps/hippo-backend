from marshmallow import Schema, fields, EXCLUDE

from app.schemas import SkillSchema


class AchievementSkillItemSchema(Schema):
    name = fields.String(required=True)
    capability_id = fields.String(required=False, missing=None)

    class Meta:
        unknown = EXCLUDE

class AchievementSchema(Schema):
    id = fields.Integer(required=False)
    description = fields.String()
    skills = fields.Nested(AchievementSkillItemSchema, many=True)

    class Meta:
        unknown = EXCLUDE
