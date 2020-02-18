from models.base_model import db
from models.tag_model import Tag, TagSchema
from marshmallow import Schema, fields, post_dump, EXCLUDE

class TagItem(db.Model):
    __tablename__ = 'tag_item'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
    score = db.Column(db.Integer)

    #relationships
    #contact = db.relationship('Contact', back_populates='tags')
    #tag = db.relationship('Tag', back_populates='contacts')
    resumes = db.relationship('ResumeItem', back_populates='tag',
                              cascade='all, delete, delete-orphan')


class TagItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    contact_id = fields.Integer(required=True)
    tag_id = fields.Integer(required=True)
    name = fields.Pluck(TagSchema, 'name', attribute='tag', dump_only=True)
    type = fields.Pluck(TagSchema, 'type', attribute='tag', dump_only=True)
    score = fields.Integer() #Decimal() throws an error in python 3.7

    class Meta:
        unknown = EXCLUDE
