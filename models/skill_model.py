from models.base_model import db
from marshmallow import Schema, fields, post_dump, EXCLUDE

# Helper table to classify capabilities
capability_skills = db.Table('capability_skills',
    db.Column('capability_id', db.String, db.ForeignKey('capability.id')),
    db.Column('skill_id', db.String, db.ForeignKey('skill.id')),
    db.PrimaryKeyConstraint(
        'capability_id',
        'skill_id',
        name='capability_skills_pk'),
)

class Skill(db.Model):
    __tablename__ = 'skill'

    #table columns
    id = db.Column(db.String, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)

    #relationships
    capabilities = db.relationship('Capability', 
                                   secondary=capability_skills,
                                   lazy='subquery',
                                   back_populates='related_skills'
                                   )

    __table_args__ = (
        db.UniqueConstraint('name', name='skill_name_uniq'),
    )

class Capability(db.Model):
    __tablename__ = 'capability'

    #table columns
    id = db.Column(db.String, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    cap_skill_id = db.Column(db.String, db.ForeignKey('skill.id'), nullable=False)

    #relationships
    related_skills = db.relationship('Skill', 
                                   secondary=capability_skills,
                                   lazy='subquery',
                                   back_populates='capabilities')
    recommended_skills = db.relationship('SkillRecommendation', 
                                         order_by='SkillRecommendation.order',
                                         cascade='all, delete')

    __table_args__ = (
        db.UniqueConstraint('name', name='capability_name_uniq'),
        db.UniqueConstraint('cap_skill_id', name='cap_skill_id_uniq'),
    )

class SkillRecommendation(db.Model):
    __tablename__ = 'capability_skill_recommendations'

    #table columns
    capability_id = db.Column(db.String, db.ForeignKey('capability.id'), nullable=False)
    skill_id = db.Column(db.String, db.ForeignKey('skill.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)

    #relationships
    skill = db.relationship('Skill')

    __table_args__ = (
        db.PrimaryKeyConstraint('capability_id', 'skill_id', name='cap_skill_rec_pk'),
        db.UniqueConstraint('capability_id', 'order', name='cap_skill_rec_order_uniq'),
    )
    

class SkillSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    capabilities = fields.List(fields.Nested(lambda: CapabilitySchema(only=('id', 'name'))), dump_only=True)

    class Meta:
        unknown = EXCLUDE

class SkillRecommendationSchema(Schema):
    capabiliity_id = fields.String(required=True, load_only=True)
    skill_id = fields.String(required=True, load_only=True)
    skill = fields.Nested(SkillSchema, dump_only=True)
    order = fields.Integer(required=True)

class CapabilitySchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    cap_skill_id = fields.String(dump_only=True)
    related_skills = fields.List(fields.Nested(SkillSchema(exclude=('capabilities',))), dump_only=True)
    recommended_skills = fields.List(fields.Nested(SkillRecommendationSchema), dump_only=True)

    class Meta:
        unknown = EXCLUDE
