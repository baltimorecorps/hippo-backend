# TODO: DELETE THIS

from models.base_model import db
import enum
from marshmallow import Schema, fields, EXCLUDE
from marshmallow_enum import EnumField


class TagType(enum.Enum):
    function = 'Function'
    skill = 'Skill'
    topic = 'Topic'


class TagStatusType(enum.Enum):
    active = 'Active'
    inactive = 'Inactive'


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(TagType, name='TagType'), nullable=False)
    status = db.Column(db.Enum(TagStatusType, name='TagStatusType'))

    #relationships
    #contacts = db.relationship('TagItem', back_populates='tag',
    #                           cascade='all, delete, delete-orphan')


class TagSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    type = EnumField(TagType, by_value=True, required=True)
    status = EnumField(TagStatusType, by_value=True)

    class Meta:
        unknown = EXCLUDE
