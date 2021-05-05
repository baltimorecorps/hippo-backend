from marshmallow import Schema, fields, EXCLUDE


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
