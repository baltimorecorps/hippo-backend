from models.base_model import db
from marshmallow import Schema, fields, post_dump, EXCLUDE

# Helper table to tag experiences with skills
experience_skills = db.Table('experience_skills',
    db.Column('experience_id', db.Integer, db.ForeignKey('experience.id')),
    db.Column('skill_id', db.String, index=True),
    db.Column('contact_id', db.Integer),
    db.PrimaryKeyConstraint(
        'experience_id',
        'skill_id',
        'contact_id',
        name='experience_skills_pk'),
    db.ForeignKeyConstraint(['skill_id', 'contact_id'],
                            ['skill_item.id', 'skill_item.contact_id']),
)

class SkillItem(db.Model):
    __tablename__ = 'skill_item'

    #table columns
    id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)

    #relationships
    contact = db.relationship('Contact')
    experiences = db.relationship('Experience',
                                  secondary=experience_skills,
                                  lazy='subquery')

    __table_args__ = (
        db.PrimaryKeyConstraint('id', 'contact_id', name='skill_item_pk'),
    )


class SkillItemSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    contact_id = fields.Integer(dump_only=True)

    class Meta:
        unknown = EXCLUDE
