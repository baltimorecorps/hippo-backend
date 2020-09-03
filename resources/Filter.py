from flask_restful import Resource, request
from flask_login import login_required
import json

from models.base_model import db
from models.contact_model import Contact, ContactSchema, ContactStage
from models.program_app_model import ProgramApp, ProgramAppSchema
from models.profile_model import (
    Profile,
    Race,
    ProfileSchema,
    RaceSchema,
    RoleChoiceSchema,
    ProgramsCompletedSchema
)

from marshmallow import Schema, fields, EXCLUDE, ValidationError
from marshmallow_enum import EnumField

from auth import (
    refresh_session,
    is_authorized_view,
    is_authorized_write,
    is_authorized_with_permission,
    unauthorized,
)


class FilterInputSchema(Schema):
    status = fields.List(fields.String(),allow_none=True)
    years_exp = fields.List(fields.String(), allow_none=True)
    job_search_status = fields.List(fields.String(), allow_none=True)
    current_job_status = fields.List(fields.String(), allow_none=True)
    current_edu_status = fields.List(fields.String(), allow_none=True)
    previous_bcorps_program = fields.List(fields.String(), allow_none=True)
    needs_help_programs = fields.List(fields.String(), allow_none=True)
    hear_about_us = fields.List(fields.String(), allow_none=True)
    race = fields.Nested(RaceSchema, allow_none=True)

class FilterOutputSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(dump_only=True)
    last_name = fields.String(dump_only=True)
    email = fields.String(dump_only=True)
    status = EnumField(ContactStage, dump_only=True)
    phone_primary = fields.String(dump_only=True)
    years_exp = fields.Pluck(ProfileSchema,
                             'years_exp',
                             attribute='profile',
                             dump_only=True)
    job_search_status = fields.Pluck(ProfileSchema,
                                     'job_search_status',
                                     attribute='profile',
                                     dump_only=True)
    programs_interested = fields.Pluck(ProgramAppSchema,
                                       'program_name',
                                       many=True,
                                       data_key='programs')

input_schema = FilterInputSchema()
output_schema = FilterOutputSchema(many=True)

def format_row(row):
    fields = [
        'id',
        'first_name',
        'last_name',
        'email',
        'phone_primary',
        'status',
        'years_exp',
        'job_search_status'
    ]
    _dict = dict(zip(fields, row))
    _dict['status'] = ContactStage(_dict['status']).name
    return _dict

class Filter(Resource):

    method_decorators = {
        'post': [login_required, refresh_session]
    }

    def post(self):

        if not is_authorized_with_permission('view:all-users'):
            return unauthorized()

        json_data = request.get_json(force=True)
        query = input_schema.load(json_data)

        try:
            data = input_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422

        if not query:
            contacts = Contact.query.filter(Contact.stage > 1)
            result = output_schema.dump(contacts)
        else:
            query = (db.session
                       .query(Contact, Profile)
                       .join(Profile)
                       .filter(Contact.stage > 1)
                       .with_entities(
                            Contact.id,
                            Contact.first_name,
                            Contact.last_name,
                            Contact.email,
                            Contact.phone_primary,
                            Contact.stage,
                            Profile.years_exp,
                            Profile.job_search_status
                      ).all())
            result = [format_row(row) for row in query]

        return {'status': 'success', 'data': result}, 201
