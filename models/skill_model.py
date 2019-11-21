from models.base_model import db
from marshmallow import Schema, fields, post_dump, EXCLUDE

class SkillItem(db.Model):
    __tablename__ = 'skill_item'

    #table columns
    id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)

    #relationships
    contact = db.relationship('Contact', back_populates='skills')

    __table_args__ = (
        db.PrimaryKeyConstraint('id', 'contact_id', name='skill_item_pk'),
    )


class SkillItemSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    contact_id = fields.Integer(required=True)

    class Meta:
        unknown = EXCLUDE
