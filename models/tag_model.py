from models.base_model import db
import enum
from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from sqlalchemy_enum34 import EnumType


class TagType(enum.Enum):
    function = 'Function'
    skill = 'Skill'
    topic = 'Topic'


class TagStatusType(enum.Enum):
    active = 'Active'
    inactive = 'Inactive'


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(EnumType(TagType, name='TagType'), nullable=False)
    status = db.Column(EnumType(TagStatusType, name='TagStatusType'))


class TagSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    type = EnumField(TagType, by_value=True, required=True)
    status = EnumType(TagStatusType, by_value=True)


class TagItem(db.Model):
    __tablename__ = "tag_item"
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    contact = db.relationship('Contact')
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=False)
    address = db.relationship('Tag')
    score = db.Column(db.DECIMAL)
    tag_item_order = db.Column(db.Integer, nullable=False)


class TagItemSchema(Schema):
    id = fields.Integer()
    contact_id = fields.Integer(required=True)
    tag_id = fields.Integer(required=True)
    score = fields.Decimal()
    tag_item_order = fields.Integer(required=True)


class ContactTagSchema(Schema):
    id = fields.Integer()
    contact_id = fields.Integer(required=True)
    tag_id = fields.Integer(required=True)
    name = fields.String(required=True)
    type = EnumField(TagType, by_value=True, required=True)
