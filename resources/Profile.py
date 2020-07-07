from flask_restful import Resource, request
from flask_login import login_required

from models.base_model import db
from models.contact_model import Contact, ContactSchema
from models.profile_model import Profile, Race, ContactAddress, RoleChoice
from marshmallow import ValidationError

from auth import (
    refresh_session,
    is_authorized_view,
    is_authorized_write,
    unauthorized
)


profile_schema = ContactSchema(exclude=['skills',
                                        'programs',
                                        'terms_agreement',
                                        'account_id',
                                        'email_primary'])


class ProfileOne(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
        'put': [login_required, refresh_session],
    }


    def get(self, contact_id):
        if not is_authorized_view(contact_id):
            return unauthorized()
            
        contact = Contact.query.get(contact_id)
        if not contact.profile:
            return {'message': 'Profile does not exist'}, 404

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

        profile = Profile(contact_id=contact_id)
        profile.addresses.append(ContactAddress(contact_id=contact_id))
        profile.race = Race(contact_id=contact_id)
        profile.roles = RoleChoice()
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
