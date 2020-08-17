from models.base_model import db
from models.contact_model import ContactSchema
from marshmallow import Schema, fields, EXCLUDE
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

class UserSession(UserMixin, db.Model):
    __tablename__ = 'user_session'

    #table columns
    # This is the session id, not the user's id
    # This means it changes every time the user starts a new session
    id = db.Column(db.String, primary_key=True)
    auth_id = db.Column(db.String, nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    jwt = db.Column(db.String(1000), nullable=False)
    expiration = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    #relationships
    contact = db.relationship('Contact')

    @hybrid_property
    def is_authenticated(self):
        return self.expiration > datetime.utcnow()


class UserSessionSchema(Schema):
    # !!! The id being load only is security-critical, because the session id
    # should not be exposed to the frontend out of the session cookie
    #
    # Anyone who gets a valid session id can functionally log in as the user
    # TODO: test this
    id = fields.String(required=True, load_only=True)

    contact = fields.Nested(ContactSchema,
                            exclude=['instructions', 'experiences'],
                            required=True)
    jwt = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE
