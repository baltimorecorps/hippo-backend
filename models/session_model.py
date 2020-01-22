from models.base_model import db
from models.contact_model import ContactSchema
from marshmallow import Schema, fields, EXCLUDE
from flask_login import UserMixin

class UserSession(UserMixin, db.Model):
    __tablename__ = 'user_session'

    #table columns
    # This is the session id, not the user's id 
    # This means it changes every time the user starts a new session
    id = db.Column(db.String, primary_key=True)
    auth_id = db.Column(db.String, nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    jwt = db.Column(db.String(1000), nullable=False)

    #relationships
    contact = db.relationship('Contact')


class UserSessionSchema(Schema):
    id = fields.String(required=True)
    contact = fields.Nested(ContactSchema, required=True)
    jwt = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE



