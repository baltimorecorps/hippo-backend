from models.base_model import db
from models.tag_model import Tag, TagSchema
from marshmallow import Schema, fields

class TagItem(db.Model):
    __tablename__ = 'tag_item'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
    score = db.Column(db.DECIMAL)

    #relationships
    contact = db.relationship('Contact', back_populates='tags')
    tag = db.relationship('Tag', back_populates='contacts')


class TagItemSchema(Schema):
    id = fields.Integer()
    contact_id = fields.Integer(required=True)
    tag_id = fields.Integer(required=True)
    name = fields.Nested(TagSchema, attribute='tag', only='type')
    type = fields.Nested(TagSchema, attribute='tag', only='type')
    score = fields.Integer() #Decimal() throws an error in python 3.7
