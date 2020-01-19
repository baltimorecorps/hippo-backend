from flask import request as reqobj #ask David why this is here
from flask_restful import Resource, request
from models.contact_model import Contact, ContactSchema
from models.email_model import Email
from models.address_model import Address
from models.base_model import db
from models.skill_model import SkillItem
from models.program_contact_model import ProgramContact
from models.program_model import Program
from .ProgramContacts import create_program_contact
from marshmallow import ValidationError
from auth import requires_auth

from .skill_utils import get_skill_id, make_skill


contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)

def add_skills(skills, contact):
    for skill in skills:
        s = SkillItem.query.get((get_skill_id(skill['name']),
                                 contact.id))
        if not s:
            s = make_skill(skill['name'], contact.id)
        contact.skills.append(s)

class ContactAll(Resource):

    def get(self):
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
        result = contact_schema.dump(contact)
        return {"status": 'success', 'data': result}, 201

class ContactAccount(Resource):
    method_decorators = {'get': [requires_auth]}
    def get(self):
        account_id = request.current_user['sub']
        contact = Contact.query.filter_by(account_id=account_id).first()
        if not contact:
            return {'message': 'Contact does not exist'}, 404
        contact = contact_schema.dump(contact)
        return {'status': 'success', 'data': contact}, 200


class ContactOne(Resource):

    def get(self, contact_id):
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404
        contact = contact_schema.dump(contact)
        return {'status': 'success', 'data': contact}, 200

    def put(self, contact_id):
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404
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
            del contact.skills[:]
            add_skills(skills, contact)

        db.session.commit()
        result = contact_schema.dump(contact)
        return {"status": 'success', 'data': result}, 200
