from flask_restful import Resource, request
from flask_login import login_required

from models.base_model import db
from models.contact_model import Contact, ContactSchema
from models.profile_model import (
    Profile,
    Race,
    ContactAddress,
    RoleChoice,
    ProgramsCompleted
)
from marshmallow import ValidationError

from auth import (
    refresh_session,
    is_authorized_view,
    is_authorized_write,
    unauthorized
)


profile_schema = ContactSchema(exclude=['skills',
                                        'programs',
                                        'program_apps',
                                        'terms_agreement',
                                        'account_id',
                                        'email_primary',
                                        'instructions'])
instructions_schema = ContactSchema(exclude=['skills',
                                             'programs',
                                             'program_apps',
                                             'phone_primary',
                                             'terms_agreement',
                                             'account_id',
                                             'email_primary',
                                             'profile'])

def create_profile(contact):
    profile = Profile(contact=contact)
    profile.addresses.append(ContactAddress(contact=contact))
    profile.race = Race(contact=contact)
    profile.roles = RoleChoice()
    profile.programs_completed = ProgramsCompleted()
    return profile

class ProfileOne(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
        'put': [login_required, refresh_session],
    }


    def get(self, contact_id):
        if not is_authorized_view(contact_id):
            return unauthorized()
        contact = Contact.query.get(contact_id)
        result = profile_schema.dump(contact)
        return {'status': 'success', 'data': result}, 200

    def post(self, contact_id):
        if not is_authorized_view(contact_id):
            return unauthorized()

        contact = Contact.query.get(contact_id)

        if not contact:
            return {'message': 'Contact does not exist'}, 404

        if contact.profile:
            return {'message': 'Profile already exists'}, 400

        profile = create_profile(contact)
        db.session.add(profile)
        db.session.commit()

        result = profile_schema.dump(contact)

        return {'status': 'success', 'data': result}, 201

    def put(self, contact_id):
        if not is_authorized_write(contact_id):
            return unauthorized()

        json_data = request.get_json(force=True)

        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404

        try:
            data = profile_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422

        profile_data = data.pop('profile', None)
        contact.update(**data)
        contact.profile.update(**profile_data)
        db.session.commit()

        result = profile_schema.dump(contact)

        return {'status': 'success', 'data': result}, 200

class ContactInstructions(Resource):

    method_decorators = {
        'get': [login_required, refresh_session],
    }

    def get(self, contact_id):
        if not is_authorized_view(contact_id):
            return unauthorized()
        contact = Contact.query.get(contact_id)
        result = instructions_schema.dump(contact)
        return {'status': 'success', 'data': result}, 200
