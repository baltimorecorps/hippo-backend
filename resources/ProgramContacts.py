from flask_restful import Resource, request
from models.program_model import Program, ProgramSchema
from models.program_contact_model import ProgramContact, ProgramContactSchema, UPDATE_FIELDS
from models.response_model import Response, ResponseSchema
from models.base_model import db
from marshmallow import ValidationError

from flask_login import login_required
from auth import (
    refresh_session, 
    is_authorized_view, 
    is_authorized_write, 

    unauthorized
)

program_contact_schema = ProgramContactSchema()
program_contacts_schema = ProgramContactSchema(many=True)

def add_responses(responses, program_contact):
    for response in responses:
        r = Response(**response)
        program_contact.responses.append(r)

def query_one_program_contact(c_id, p_id):
    return (ProgramContact.query
                          .filter_by(contact_id=c_id,program_id=p_id)
                          .first())

def create_program_contact(contact_id, program_id=1, **data):
    program_contact = query_one_program_contact(contact_id, program_id)
    if program_contact:
        return {'message': 'Record already exists'}, 400
    responses = data.pop('responses', None)
    data['contact_id'] = contact_id
    data['program_id'] = program_id
    program_contact = ProgramContact(**data)
    if responses:
        add_responses(responses, program_contact)
    db.session.add(program_contact)
    db.session.commit()
    result = program_contact_schema.dump(program_contact)
    return  result

class ProgramContactAll(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
        'post': [login_required, refresh_session],
    }

    def get(self,contact_id):
        if not is_authorized_view(contact_id): 
            return unauthorized()

        program_contacts = ProgramContact.query.filter_by(contact_id=contact_id)
        result = program_contacts_schema.dump(program_contacts)
        return {'status': 'success', 'data': result}, 200

    def post(self, contact_id):
        if not is_authorized_write(contact_id): 
            return unauthorized()

        #retrieve and parse request data
        json_data = request.get_json(force=True)
        try:
            data = program_contact_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No data provided to update'}, 400

        # checks to see if there's an existing program_contact record
        program = data.pop('program_id')
        contact = data.pop('contact_id')
        result = create_program_contact(contact_id, program_id=program, **data)
        return {"status": 'success', 'data': result}, 201

class ProgramContactOne(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
        'post': [login_required, refresh_session],
        'put': [login_required, refresh_session],
    }

    def get(self, contact_id, program_id):
        if not is_authorized_view(contact_id): 
            return unauthorized()

        program_contact = query_one_program_contact(contact_id, program_id)
        if not program_contact:
            return {'message': 'Record does not exist'}, 404
        result = program_contact_schema.dump(program_contact)
        return {'status': 'success', 'data': result}, 200

    def put(self, contact_id, program_id):
        if not is_authorized_write(contact_id): 
            return unauthorized()

        #retreives and parses request data
        json = request.get_json(force=True)
        try:
            data = program_contact_schema.load(json, partial=True)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No data provided to update'}, 400

        # checks to make sure the record exists
        program_contact = query_one_program_contact(contact_id, program_id)
        if not program_contact:
            return {'message': 'Record does not exist'}, 404

        # updates program_contact record and related response records
        responses = data.pop('responses', None)
        for k,v in data.items():
            if k in UPDATE_FIELDS:
                setattr(program_contact, k, v)
        if responses:
            del program_contact.responses[:]
            add_responses(responses, program_contact)

        db.session.commit()
        result = program_contact_schema.dump(program_contact)
        return {"status": 'success', 'data': result}, 200

    def delete(self, contact_id, program_id):
        if not is_authorized_write(contact_id): 
            return unauthorized()

        program_contact = query_one_program_contact(contact_id, program_id)
        if not program_contact:
            return {'message': 'Program contact does not exist'}, 404
        db.session.delete(program_contact)
        db.session.commit()
        return {"status": 'success'}, 200
