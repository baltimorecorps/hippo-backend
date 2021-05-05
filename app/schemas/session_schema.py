from marshmallow import Schema, fields, EXCLUDE

from app.schemas import ContactSchema, ContactShortSchema


class UserSessionSchema(Schema):
    # !!! The id being load only is security-critical, because the session id
    # should not be exposed to the frontend out of the session cookie
    #
    # Anyone who gets a valid session id can functionally log in as the user
    # TODO: test this
    id = fields.String(required=True, load_only=True)

    contact = fields.Nested(ContactShortSchema, required=True)
    jwt = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE
