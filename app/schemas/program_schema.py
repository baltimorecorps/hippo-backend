from marshmallow import Schema, fields, EXCLUDE


class ProgramSchema(Schema):
    id = fields.Integer()
    name = fields.String()

    class Meta:
        unknown = EXCLUDE


class ProgramAppSchema(Schema):
    id = fields.Integer()
    program = fields.Nested(ProgramSchema)
    status = fields.String(dump_only=True)
    is_approved = fields.Boolean(allow_none=True)
    is_interested = fields.Boolean(allow_none=True)
    decision_date = fields.Date(dump_only=True)

    # For use in FilterOutputSchema, exclude from other Schemas
    program_name = fields.Pluck(
        ProgramSchema,
        'name',
        dump_only=True,
        attribute='program'
    )

    class Meta:
        unknown = EXCLUDE
