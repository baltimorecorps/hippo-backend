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
    american_indian = db.Column(db.Boolean, default=False)
    asian = db.Column(db.Boolean, default=False)
    black = db.Column(db.Boolean, default=False)
    hawaiian = db.Column(db.Boolean, default=False)
    hispanic = db.Column(db.Boolean, default=False)
    south_asian = db.Column(db.Boolean, default=False)
    white = db.Column(db.Boolean, default=False)
    not_listed = db.Column(db.Boolean, default=False)
    race_other = db.Column(db.String)
    race_all = db.Column(db.String, default='No Response')

    #relationships
    contact = db.relationship('Contact', back_populates='race')
    profile = db.relationship('Profile', back_populates='race')

    #methods
    def update(self, **update_dict):
        UPDATE_FIELDS = {
            'american_indian': 'American Indian or Alaskan Native',
            'asian': 'Asian',
            'black': 'Black or African Descent',
            'hispanic': 'Hispanic or Latinx',
            'hawaiian': 'Native Hawaiian or Other Pacific Islander',
            'south_asian': 'South Asian',
            'white': 'White',
            'not_listed': 'Not Listed',
            'race_other': ''
        }
        race_list = []
        for field, value in update_dict.items():
            if field in UPDATE_FIELDS:
                setattr(self, field, value)
                if value == True:
                    race_list.append(UPDATE_FIELDS[field])
        if not race_list:
            race_all = 'No Response'
        else:
            race_all = ";".join(sorted(race_list))
        self.race_all = race_all

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
    advocacy_public_policy = db.Column(db.Boolean, default=False)
    community_engagement_outreach = db.Column(db.Boolean, default=False)
    data_analysis = db.Column(db.Boolean, default=False)
    fundraising_development = db.Column(db.Boolean, default=False)
    marketing_public_relations = db.Column(db.Boolean, default=False)
    program_management = db.Column(db.Boolean, default=False)

    #relationships
    profile = db.relationship('Profile', back_populates='roles')

    # calculated fields
    @hybrid_property
    def role_choice_complete(self):
        return (
            self.advocacy_public_policy
            or self.community_engagement_outreach
            or self.data_analysis
            or self.fundraising_development
            or self.marketing_public_relation
            or self.program_management
        )

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

class ProgramsCompleted(db.Model):
    __tablename__ = 'programs_completed'

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer,
                           db.ForeignKey('profile.id'),
                           nullable=False)
    fellowship = db.Column(db.Boolean, default=False)
    mayoral_fellowship = db.Column(db.Boolean, default=False)
    public_allies = db.Column(db.Boolean, default=False)
    kiva = db.Column(db.Boolean, default=False)
    civic_innovators = db.Column(db.Boolean, default=False)
    elevation_awards = db.Column(db.Boolean, default=False)

    #relationships
    profile = db.relationship('Profile', back_populates='programs_completed')

    #methods
    def update(self, **update_dict):
        UPDATE_FIELDS = [
            'fellowship',
            'mayoral_fellowship',
            'public_allies',
            'kiva',
            'civic_innovators',
            'elevation_awards',
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
    needs_help_programs = db.Column(db.Boolean)
    hear_about_us = db.Column(db.String)
    hear_about_us_other = db.Column(db.String)
    value_question1 = db.Column(db.String)
    value_question2 = db.Column(db.String)

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
    programs_completed = db.relationship('ProgramsCompleted',
                                         back_populates='profile',
                                         cascade='all, delete, delete-orphan',
                                         uselist=False)
    contact = db.relationship('Contact', back_populates='profile')

    # calculated fields
    @hybrid_property
    def roles_list(self):
        role_dict = {
            'advocacy_public_policy': 'Advocacy and Public Policy',
            'community_engagement_outreach': 'Community Engagement and Outreach',
            'data_analysis': 'Data Analysis',
            'fundraising_development': 'Fundraising and Development',
            'marketing_public_relations':  'Marketing and Public Relations',
            'program_management': 'Program Management',
        }
        roles_selected = [role_dict[k] for k,v in self.roles.__dict__.items()
                          if k in role_dict.keys() and v==True]
        return roles_selected

    @hybrid_property
    def candidate_info_complete(self):
        if self.address_primary:
            return (
                self.address_primary.street1 is not None
                and self.address_primary.city is not None
                and self.address_primary.state is not None
                and self.address_primary.country is not None
                and self.address_primary.zip_code is not None
            )
        else:
            return False

    @hybrid_property
    def value_alignment_complete(self):
        return (self.value_question1 is not None
                and self.value_question2 is not None)

    @hybrid_property
    def interests_and_goals_complete(self):
        return (
            self.years_exp is not None
            and self.job_search_status is not None
            and self.current_job_status is not None
            and self.current_edu_status is not None
        )

    @hybrid_property
    def programs_and_eligibility_complete(self):
        if self.contact.program_apps:
            programs = [p for p in self.contact.program_apps
                        if p.is_interested]
        else:
            programs = []

        return self.needs_help_programs or (len(programs) > 0)

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
            'previous_bcorps_program',
            'needs_help_programs',
            'hear_about_us',
            'hear_about_us_other',
            'value_question1',
            'value_question2',
        ]

        address_data = update_dict.pop('address_primary', None)
        race_data = update_dict.pop('race', None)
        role_data = update_dict.pop('roles', None)
        programs_data = update_dict.pop('programs_completed', None)

        for field, value in update_dict.items():
            if field in UPDATE_FIELDS:
                setattr(self, field, value)

        if address_data:
            self.address_primary.update(**address_data)
        if race_data:
            self.race.update(**race_data)
        if role_data:
            self.roles.update(**role_data)
        if programs_data:
            self.programs_completed.update(**programs_data)

class RaceSchema(Schema):

    american_indian = fields.Boolean(allow_none=True)
    asian = fields.Boolean(allow_none=True)
    black = fields.Boolean(allow_none=True)
    hawaiian = fields.Boolean(allow_none=True)
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
    is_primary = fields.Boolean(allow_none=True, dump_only=True)

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

class ProgramsCompletedSchema(Schema):

    fellowship = fields.Boolean(allow_none=True)
    mayoral_fellowship = fields.Boolean(allow_none=True)
    public_allies = fields.Boolean(allow_none=True)
    kiva = fields.Boolean(allow_none=True)
    civic_innovators = fields.Boolean(allow_none=True)
    elevation_awards = fields.Boolean(allow_none=True)

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
    value_question1 = fields.String(allow_none=True)
    value_question2 = fields.String(allow_none=True)
    hear_about_us = fields.String(allow_none=True)
    hear_about_us_other = fields.String(allow_none=True)
    previous_bcorps_program = fields.String(allow_none=True)
    needs_help_programs = fields.Boolean(allow_none=True)
    address_primary = fields.Nested(ContactAddressSchema, allow_none=True)
    race = fields.Nested(RaceSchema, allow_none=True)
    roles = fields.Nested(RoleChoiceSchema, allow_none=True)
    programs_completed = fields.Nested(ProgramsCompletedSchema,
                                       allow_none=True)

    class Meta:
        unknown = EXCLUDE
