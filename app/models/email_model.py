import enum

from app.models import db


class Type(enum.Enum):
    personal = 'Personal'
    work = 'Work'


class Email(db.Model):
    __tablename__ = 'email'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(Type, name='EmailType'))

    #relationships
    contact = db.relationship('Contact', back_populates='email_primary')
