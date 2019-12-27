from models.base_model import db
from marshmallow import Schema, fields, post_dump, EXCLUDE


class Program(db.Model):
    __tablename__ = 'skill_item'

    #table columns
    id = db.Column(db.String, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)

    #relationship fields
    cycles = db.relationship('Program', back_populates='program',
                             cascade='all, delete, delete-orphan')

class Program(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE
