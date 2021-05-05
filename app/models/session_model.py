from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from app.models import db


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
