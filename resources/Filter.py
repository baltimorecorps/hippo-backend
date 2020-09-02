from flask_restful import Resource, request
from flask_login import login_required

from models.base_model import db
from models.contact_model import Contact, ContactSchema
from models.program_app_model import ProgramAppSchema
from models.profile_model import (
    ProfileSchema,
    RaceSchema,
    RoleChoiceSchema,
    ProgramsCompletedSchema
)

from marshmallow import Schema, fields, EXCLUDE

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

class Filter(Resource):

    method_decorators = {
        'post': [login_required, refresh_session]
    }

    def post(self):

        if not is_authorized_with_permission('view:all-users'):
            return unauthorized()

        query = request.get_json(force=True)
        if not query:
            contacts = Contact.query.filter(Contact.stage > 1)
        else:
            contacts = Contact.query.filter(Contact.stage > 1)

        result = output_schema.dump(contacts)

        return {'status': 'success', 'data': result}, 201
