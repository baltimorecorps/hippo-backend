from models.base_model import db
from models.tag_model import Tag, TagSchema
from marshmallow import Schema, fields, post_dump

class TagItem(db.Model):
    __tablename__ = 'tag_item'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
    score = db.Column(db.Integer)

    #relationships
    contact = db.relationship('Contact', back_populates='tags')
    tag = db.relationship('Tag', back_populates='contacts')
    resumes = db.relationship('ResumeItem', back_populates='tag',
                              cascade='all, delete, delete-orphan')


class TagItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    contact_id = fields.Integer(required=True)
    tag_id = fields.Integer(required=True)
    tag = fields.Nested(TagSchema, only=['name', 'type'], dump_only=True)
    score = fields.Integer() #Decimal() throws an error in python 3.7

    @post_dump
    def flatten_tag(self, data, **kwargs): 
        """
        Pull the fields from the nested 'tag' object up into the main tag item
        object.
        """
        tag = data['tag']
        data['name'] = tag['name']
        data['type'] = tag['type']
        del data['tag']
        return data
