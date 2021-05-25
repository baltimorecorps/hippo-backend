# from flask import request as reqobj #ask David why this is here
# from flask import current_app
from flask_restful import Resource, request
from flask_login import login_user, current_user, login_required
from marshmallow import ValidationError

from app.models import (
    db,
    Contact,
    ContactStage,
    Email,
    EmailType,
    Program,
    Skill,
)
from app.schemas import (
    ContactSchema,
    ContactShortSchema,
)
from app.auth import (
    validate_jwt,
    create_session,
    refresh_session,
    is_authorized_view,
    is_authorized_write,
    is_authorized_with_permission,
    unauthorized,
)
from app.resources.skill_utils import get_skill_id, get_or_make_skill
from app.resources.profile_resource import create_profile


contact_schema = ContactSchema(exclude=['instructions',
                                        'experiences'])
contacts_schema = ContactSchema(exclude=['instructions',
                                         'experiences'],
                                many=True)
contacts_short_schema = ContactShortSchema(many=True)
contact_program_schema = ContactSchema(
    many=True,
    exclude=['skills',
             'program_apps',
             'profile',
             'instructions',
             'experiences',
             'email_primary',
             'email']
)
contact_full_schema = ContactSchema()


def add_skills(skills, contact):
    for skill_data in skills:
        skill = get_or_make_skill(skill_data['name'])
        contact.add_skill(skill)

def sync_skills(skills, contact):
    add_skills(skills, contact)

    current_skills = {s['name'] for s in skills}
    for skill_item in contact.skill_items:
        if skill_item.skill.name not in current_skills:
            skill_item.deleted = True

class ContactAll(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
        'post': [validate_jwt],
    }

    def post(self):
        json_data = request.get_json(force=True)
        # Validate and deserialize input

        try:
            data = contact_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No input data provided'}, 400
        if data['account_id'] != request.jwt['sub']:
            return {'message': 'Account id does not match post!'}, 400

        existing_contact = (
            Contact.query
                   .filter_by(account_id=data['account_id'])
                   .first()
        )
        if existing_contact:
            return {'message': 'A contact with this account already exists'}, 400

        email_primary = data.pop('email_primary', None)
        email = data.get('email', None)

        contact = Contact(**data)
        if email_primary:
            contact.email_primary = Email(**email_primary)
            contact.email = email_primary['email']
        elif email:
            email_primary = {
                'email': email,
                'is_primary': True,
                'type': EmailType('Work')
            }
            contact.email_primary = Email(**email_primary)
        else:
            return {'message': 'No email provided'}, 400

        create_profile(contact)
        db.session.add(contact)
        db.session.commit()

        '''
        program_contact_data = {
            'stage': 1,
            'program_id': 1
        }
        create_program_contact(contact.id, **program_contact_data)
        db.session.commit()
        '''

        user_session = create_session(contact.id, request.jwt)
        login_user(user_session)

        result = contact_schema.dump(contact)
        return {"status": 'success', 'data': result}, 201

class ContactShort(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
    }

    def get(self):
        if not is_authorized_with_permission('view:all-users'):
            return unauthorized()

        status = request.args.get('status')
        status_list = ContactStage.__members__
        if not status:
            contacts = Contact.query.all()
        elif status not in status_list:
            return {'message':
                    f'{status} is not a valid stage '
                    f'choose an option from this list: {status_list}'}, 400
        else:
            contacts = (Contact.query
                               .filter_by(stage=ContactStage[status].value))

        contacts = contacts_short_schema.dump(contacts)
        return {'status': 'success', 'data': contacts}, 200


class ContactAccount(Resource):
    method_decorators = {
        'get': [validate_jwt],
    }

    def get(self):
        account_id = request.jwt['sub']
        contact = Contact.query.filter_by(account_id=account_id).first()
        if not contact:
            return {'message': 'Contact does not exist'}, 404
        contact = contact_schema.dump(contact)
        return {'status': 'success', 'data': contact}, 200


class ContactOne(Resource):
    method_decorators = {
        'get': [], #used to be [login_required, refresh_session]
        'put': [login_required, refresh_session],
        'delete': [login_required, refresh_session]
    }

    def get(self, contact_id):
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404

        # TODO: Create employer permission to restore AuthZ
        #if not is_authorized_view(contact.id):
        #    return unauthorized()

        contact = contact_schema.dump(contact)
        return {'status': 'success', 'data': contact}, 200

    def put(self, contact_id):
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404
        if not is_authorized_write(contact.id):
            return unauthorized()
        json_data = request.get_json(force=True)
        try:
            data = contact_schema.load(json_data, partial=True)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No input data provided'}, 400
        email = data.pop('email_primary', None)
        email_list = data.pop('emails', None)
        skills = data.pop('skills', None)

        contact.update(**data)

        if email:
            del contact.emails[:]
            contact.email_primary = Email(**email)

        if skills:
            sync_skills(skills, contact)

        db.session.commit()
        result = contact_schema.dump(contact)
        return {"status": 'success', 'data': result}, 200

    def delete(self, contact_id):
        if not is_authorized_with_permission('delete:all-users'):
            return unauthorized()
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404
        db.session.delete(contact)
        db.session.commit()
        return {"status": 'success'}, 200

class ContactFull(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
    }

    def get(self, contact_id):
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404

        if not is_authorized_view(contact.id):
            return unauthorized()

        contact = contact_full_schema.dump(contact)
        return {'status': 'success', 'data': contact}, 200

class ContactApproveMany(Resource):
    method_decorators = {
        'post': [login_required, refresh_session]
    }

    def post(self):
        if not is_authorized_with_permission('write:all-users'):
            return unauthorized()

        json_data = request.get_json(force=True)
        try:
            data = contacts_short_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No data provided to update'}, 400

        # Check that all of the contacts are in the db
        contact_ids = [c['id'] for c in data]
        contacts = Contact.query.filter(Contact.id.in_(contact_ids)).all()
        if len(data) != len(contacts):
            return {'message': ("Payload contained contacts "
                                "that couldn't be found")}, 404

        # Update the stage of each contact
        for contact in contacts:
            contact.stage = ContactStage.approved.value
        db.session.commit()

        # Format and return the contacts
        result = contacts_short_schema.dump(contacts)
        return {'status': 'success', 'data': result}, 201
