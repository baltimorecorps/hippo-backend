from flask_restful import Resource, request
from flask_login import login_required
import json

from resources.skill_utils import get_skill_id

from models.base_model import db
from models.contact_model import Contact, ContactSchema, ContactStage
from models.program_app_model import ProgramApp, ProgramAppSchema
from models.skill_item_model import ContactSkill
from models.profile_model import (
    Profile,
    Race,
    RoleChoice,
    ProgramsCompleted,
    ContactAddress,
    ProfileSchema,
    RoleChoiceSchema,
    ProgramsCompletedSchema,
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
    skills = fields.List(fields.String(), allow_none=True)
    hear_about_us = fields.List(fields.String(), allow_none=True)
    roles = fields.Nested(RoleChoiceSchema, allow_none=True)
    programs_completed = fields.Nested(ProgramsCompletedSchema, allow_none=True)
    program_apps = fields.Nested(ProgramAppSchema,
                                 many=True,
                                 allow_none=True)

    class Meta:
        unknown = EXCLUDE

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
        'job_search_status',
        'gender',
        'city',
        'state',
        'race'
    ]
    _dict = dict(zip(fields, row))
    if _dict['race']:
        _dict['race'] = _dict['race'].split(';')
    else:
        _dict['race'] = ['No Response']
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

        q = (db.session
                .query(Contact)
                .join(Contact.profile)
                .join(Contact.race)
                .join(Contact.address_primary)
                .with_entities(
                    Contact.id,
                    Contact.first_name,
                    Contact.last_name,
                    Contact.email,
                    Contact.phone_primary,
                    Contact.stage,
                    Profile.years_exp,
                    Profile.job_search_status,
                    Profile.current_edu_status,
                    Profile.gender,
                    ContactAddress.city,
                    ContactAddress.state,
                    Race.race_all,
                ))

        if not query:
            q = q.filter(Contact.stage > 1)
        else:
            # pops out stage and updates query with stage
            status_list = query.pop('status', None)
            if status_list == ['submitted']:
                q = q.filter(Contact.stage == 2)
            elif status_list == ['approved']:
                q = q.filter(Contact.stage == 3)
            else:
                q = q.filter(Contact.stage > 1)

            # pops out roles and adds them to the filter
            roles = query.pop('roles', None)
            if roles:
                q = q.join(Profile.roles)
                for r in roles:
                    q = q.filter(getattr(RoleChoice, r)==roles[r])

            # pops out programs_completed and adds them to the filter
            p_complete = query.pop('programs_completed', None)
            if p_complete:
                q = q.join(Profile.programs_completed)
                for p in p_complete:
                    q = q.filter(getattr(ProgramsCompleted, p)==p_complete[p])

            # pops out program_apps and adds them to the filter
            app_params = query.pop('program_apps', None)
            if app_params:
                programs = [app['program']['id'] for app in app_params]
                # uses subquery to prevent duplicate contacts
                # from being returned
                subq = (db.session
                          .query(ProgramApp.contact_id)
                          .filter(ProgramApp.program_id.in_(programs))
                          .filter(ProgramApp.is_interested==True)
                          .subquery())
                q = q.filter(Contact.id.in_(subq))

            # pops out skills and adds them to the filter
            skill_params = query.pop('skills', None)
            if skill_params:
                skills = [get_skill_id(skill) for skill in skill_params]
                # uses subquery to prevent duplicate contacts
                # from being returned
                subq = (db.session
                          .query(ContactSkill.contact_id)
                          .filter(ContactSkill.skill_id.in_(skills))
                          .filter(ContactSkill.deleted==False)
                          .subquery())
                q = q.filter(Contact.id.in_(subq))

            # iteratively adds query parameters to query for Profile
            for param in query:
                q = q.filter(getattr(Profile, param).in_(query[param]))

        result = [format_row(row) for row in q.all()]

        return {'status': 'success', 'data': result}, 201
