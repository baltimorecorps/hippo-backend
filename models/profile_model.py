import enum
from models.base_model import db
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields, EXCLUDE


class Race(db.Model):
    __tablename__ = 'race'

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer,
                           db.ForeignKey('contact.id'),
                           nullable=False)
    profile_id = db.Column(db.Integer,
                           db.ForeignKey('profile.id'),
                           nullable=False)
    american_indian = db.Column(db.Boolean)
    asian = db.Column(db.Boolean)
    black = db.Column(db.Boolean)
    hawaiin = db.Column(db.Boolean)
    hispanic = db.Column(db.Boolean)
    south_asian = db.Column(db.Boolean)
    white = db.Column(db.Boolean)
    not_listed = db.Column(db.Boolean)
    race_other = db.Column(db.String)

    #relationships
    contact = db.relationship('Contact', back_populates='race')
    profile = db.relationship('Profile', back_populates='race')

    #methods
    def update(self, **update_dict):
        UPDATE_FIELDS = [
            'american_indian',
            'asian',
            'black',
            'hawaiin',
            'hispanic',
            'south_asian',
            'white',
            'not_listed',
            'race_other'
        ]
        for field, value in update_dict.items():
            if field in UPDATE_FIELDS:
                setattr(self, field, value)

class ContactAddress(db.Model):
    __tablename__ = 'contact_address'

    #table columns
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer,
                           db.ForeignKey('contact.id'),
                           nullable=False)
    profile_id = db.Column(db.Integer,
                           db.ForeignKey('profile.id'),
                           nullable=False)
    is_primary = db.Column(db.Boolean, default=True)
    street1 = db.Column(db.String)
    street2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    zip_code = db.Column(db.String)

    #relationships
    contact = db.relationship('Contact', back_populates='addresses')
    profile = db.relationship('Profile', back_populates='addresses')

    #methods
    def update(self, **update_dict):
        UPDATE_FIELDS = [
            'street1',
            'street2',
            'city',
            'state',
            'country',
            'zip_code',
        ]
        for field, value in update_dict.items():
            if field in UPDATE_FIELDS:
                setattr(self, field, value)

class RoleChoice(db.Model):
    __tablename__ = 'role_choice'

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer,
                           db.ForeignKey('profile.id'),
                           nullable=False)
    advocacy_public_policy = db.Column(db.Boolean)
    community_engagement_outreach = db.Column(db.Boolean)
    data_analysis = db.Column(db.Boolean)
    fundraising_development = db.Column(db.Boolean)
    marketing_public_relations = db.Column(db.Boolean)
    program_management = db.Column(db.Boolean)

    #relationships
    profile = db.relationship('Profile', back_populates='roles')

    #methods
    def update(self, **update_dict):
        UPDATE_FIELDS = [
            'advocacy_public_policy',
            'community_engagement_outreach',
            'data_analysis',
            'fundraising_development',
            'marketing_public_relations',
            'program_management',
        ]
        for field, value in update_dict.items():
            if field in UPDATE_FIELDS:
                setattr(self, field, value)

class Profile(db.Model):
    __tablename__ = 'profile'

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer,
                           db.ForeignKey('contact.id'),
                           nullable=False)
    gender = db.Column(db.String)
    gender_other = db.Column(db.String)
    pronoun = db.Column(db.String)
    pronoun_other = db.Column(db.String)
    years_exp = db.Column(db.String)
    job_search_status = db.Column(db.String)
    current_job_status = db.Column(db.String)
    current_edu_status = db.Column(db.String)
    previous_bcorps_program = db.Column(db.String)

    #relationships
    race = db.relationship('Race',
                           back_populates='profile',
                           cascade='all, delete, delete-orphan',
                           uselist=False)
    address_primary = db.relationship('ContactAddress',
                                      primaryjoin=db.and_(
                                            id == ContactAddress.profile_id,
                                            ContactAddress.is_primary == True),
                                      back_populates='profile',
                                      uselist=False)
    addresses = db.relationship('ContactAddress',
                                back_populates='profile',
                                cascade='all, delete, delete-orphan')
    roles = db.relationship('RoleChoice',
                            back_populates='profile',
                            cascade='all, delete, delete-orphan',
                            uselist=False)
    contact = db.relationship('Contact', back_populates='profile')

    #methods
    def update(self, **update_dict):
        UPDATE_FIELDS = [
            'gender',
            'gender_other',
            'pronoun',
            'pronoun_other',
            'years_exp',
            'job_search_status',
            'current_job_status',
            'current_edu_status',
            'previous_bcorps_program'
        ]

        address_data = update_dict.pop('address_primary', None)
        race_data = update_dict.pop('race', None)
        role_data = update_dict.pop('roles', None)

        for field, value in update_dict.items():
            if field in UPDATE_FIELDS:
                setattr(self, field, value)

        self.address_primary.update(**address_data)
        self.race.update(**race_data)
        self.roles.update(**role_data)

class RaceSchema(Schema):

    american_indian = fields.Boolean(allow_none=True)
    asian = fields.Boolean(allow_none=True)
    black = fields.Boolean(allow_none=True)
    hawaiin = fields.Boolean(allow_none=True)
    hispanic = fields.Boolean(allow_none=True)
    south_asian = fields.Boolean(allow_none=True)
    white = fields.Boolean(allow_none=True)
    not_listed = fields.Boolean(allow_none=True)
    race_other = fields.String(allow_none=True)

    class Meta:
        unknown = EXCLUDE

class ContactAddressSchema(Schema):

    street1 = fields.String(allow_none=True)
    street2 = fields.String(allow_none=True)
    city = fields.String(allow_none=True)
    state = fields.String(allow_none=True)
    country = fields.String(allow_none=True)
    zip_code = fields.String(allow_none=True)

    class Meta:
        unknown = EXCLUDE

class RoleChoiceSchema(Schema):

    advocacy_public_policy = fields.Boolean(allow_none=True)
    community_engagement_outreach = fields.Boolean(allow_none=True)
    data_analysis = fields.Boolean(allow_none=True)
    fundraising_development = fields.Boolean(allow_none=True)
    marketing_public_relations = fields.Boolean(allow_none=True)
    program_management = fields.Boolean(allow_none=True)

    class Meta:
        unknown = EXCLUDE

class ProfileSchema(Schema):

    id = fields.Integer(dump_only=True)
    gender = fields.String(allow_none=True)
    gender_other = fields.String(allow_none=True)
    pronoun = fields.String(allow_none=True)
    pronoun_other = fields.String(allow_none=True)
    years_exp = fields.String(allow_none=True)
    job_search_status = fields.String(allow_none=True)
    current_job_status = fields.String(allow_none=True)
    current_edu_status = fields.String(allow_none=True)
    previous_bcorps_program = fields.String(allow_none=True)
    address_primary = fields.Nested(ContactAddressSchema)
    race = fields.Nested(RaceSchema)
    roles = fields.Nested(RoleChoiceSchema)

    class Meta:
        unknown = EXCLUDE
