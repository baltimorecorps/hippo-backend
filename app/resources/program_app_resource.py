from flask_restful import Resource, request
from flask_login import login_required
from marshmallow import ValidationError

from app.schemas import ProgramSchema, ContactSchema
from app.models import (
    db,
    Program,
    Contact,
    ProgramApp,
)
from app.auth import (
    refresh_session,
    is_authorized_view,
    is_authorized_write,
    is_authorized_with_permission,
    unauthorized
)

program_app_schema = ContactSchema(exclude=[
    'email_primary',
    'skills',
    'profile',
    'instructions',
    'experiences'
])

program_app_many_schema = ContactSchema(
    many=True,
    exclude=[
        'email_primary',
        'skills',
        'profile',
        'instructions',
        'experiences'
])

class ContactProgramAppsOne(Resource):
    method_decorators = {
        'get': [login_required, refresh_session]
    }

    def get(self, contact_id):

        if not is_authorized_view(contact_id):
            return unauthorized()

        contact = Contact.query.get(contact_id)
        result = program_app_schema.dump(contact)
        return {'status': 'success', 'data': result}, 200

class ContactProgramAppsAll(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
    }

    def get(self):
        if not is_authorized_with_permission('view:all-users'):
            return unauthorized()

        approved_arg = request.args.get('is_approved')
        if not approved_arg:
            contacts = Contact.query.all()
        else:
            if approved_arg == 'true':
                contacts = Contact.query.filter(Contact.stage>=3)
            elif approved_arg == 'false':
                contacts = Contact.query.filter(Contact.stage<3)
        contacts = program_app_many_schema.dump(contacts)
        return {'status': 'success', 'data': contacts}, 200

class ContactProgramAppsInterested(Resource):
    method_decorators = {
        'put': [login_required, refresh_session]
    }

    def put(self, contact_id):
        if not is_authorized_write(contact_id):
            return unauthorized()

        json_data = request.get_json(force=True)

        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404

        try:
            data_raw = program_app_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422

        data = data_raw.pop('program_apps', None)

        if not data:
            return {'message': 'No program data provided'}, 404

        for item in data:
            app = (ProgramApp.query
                             .filter_by(contact_id=contact_id,
                                        program_id=item['program']['id'])
                             .first())

            if app:
                item.pop('is_approved', None)
                app.update(**item)
            else:
                new_app = ProgramApp(
                    contact_id = contact_id,
                    program_id = item['program']['id'],
                    is_interested = item['is_interested']
                )
                contact.program_apps.append(new_app)

        db.session.add(contact)
        db.session.commit()
        result = program_app_schema.dump(contact)
        return {'status': 'success', 'data': result}, 200
