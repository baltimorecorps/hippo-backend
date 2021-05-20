from marshmallow import Schema, fields, EXCLUDE
from marshmallow_enum import EnumField

from app.models import EmailType


class EmailSchema(Schema):
    id = fields.Integer(dump_only=True)
    is_primary = fields.Boolean()
    email = fields.Email(required=True)
    type = EnumField(EmailType, by_value=True)

    class Meta:
        unknown = EXCLUDE
