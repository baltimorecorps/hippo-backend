from flask import request as reqobj #ask David why this is here
from flask import current_app
from flask_restful import Resource, request
from flask_login import login_user, current_user, login_required
from models.contact_model import Contact, ContactSchema
from models.email_model import Email
from models.address_model import Address
from models.base_model import db
from models.program_contact_model import ProgramContact
from models.program_model import Program
from .ProgramContacts import create_program_contact
from .Trello_Intake_Talent import add_new_talent_card
from marshmallow import ValidationError
from auth import (
    validate_jwt, 
    create_session, 
    refresh_session, 
    is_authorized_view, 
    is_authorized_write, 
    is_authorized_with_permission, 
    unauthorized
)

from models.skill_model import Skill
from .skill_utils import get_skill_id, get_or_make_skill


contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)

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

    def get(self):
        if not is_authorized_with_permission('view:all-users'): 
            return unauthorized()

        contacts = Contact.query.all()

        contacts = contacts_schema.dump(contacts)
        return {'status': 'success', 'data': contacts}, 200

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

        email = data.pop('email_primary', None)
        contact = Contact(**data)
        if email:
            contact.email_primary = Email(**email)
        db.session.add(contact)
        db.session.commit()
        program_contact_data = {
            'stage': 1,
            'program_id': 1
        }
        create_program_contact(contact.id, **program_contact_data)
        add_new_talent_card(contact.id)

        user_session = create_session(contact.id, request.jwt)
        login_user(user_session)

        result = contact_schema.dump(contact)
        return {"status": 'success', 'data': result}, 201

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
        'get': [login_required, refresh_session],
        'put': [login_required, refresh_session],
    }

    def get(self, contact_id):
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404
        if not is_authorized_view(contact.id): 
            return unauthorized()
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

        for k,v in data.items():
            setattr(contact, k, v)

        if email:
            del contact.emails[:]
            contact.email_primary = Email(**email)

        if skills:
            sync_skills(skills, contact)

        db.session.commit()
        result = contact_schema.dump(contact)
        return {"status": 'success', 'data': result}, 200

    def delete(self, contact_id):
        config = current_app.config
        secret_token = config['CONTACT_DELETE_TOKEN']
        request_token = request.args.get('token')
        if not request_token:
            return {'message': 'No token supplied with request'}, 400
        if request_token != secret_token:
            return {'message': "This token isn't authorized "}, 403
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404
        db.session.delete(contact)
        db.session.commit()
        return {"status": 'success'}, 200
