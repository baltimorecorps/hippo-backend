from marshmallow import Schema, fields, post_dump, EXCLUDE


class SkillSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE

class SkillRecommendationSchema(Schema):
    capability_id = fields.String(required=True, load_only=True)
    skill_id = fields.String(required=True, load_only=True)
    skill = fields.Nested(SkillSchema, dump_only=True)
    order = fields.Integer(required=True)

class CapabilitySchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    related_skills = fields.List(
        fields.Nested(SkillSchema(only=('id', 'name'))), dump_only=True)
    recommended_skills = fields.List(
        fields.Nested(SkillRecommendationSchema), dump_only=True)

    class Meta:
        unknown = EXCLUDE
