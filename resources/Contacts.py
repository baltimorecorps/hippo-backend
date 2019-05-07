from flask_restful import Resource, request
from models.contact_model import Contact, ContactSchema
from models.email_model import Email
from models.address_model import Address
from models.base_model import db


contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)


class ContactAll(Resource):

    def get(self):
        contacts = Contact.query.all()
        contacts = contacts_schema.dump(contacts).data
        return {'status': 'success', 'data': contacts}, 200

    def post(self):
        json_data = request.get_json(force=True)
        # Validate and deserialize input
        data, errors = contact_schema.load(json_data)
        if not data:
            return {'message': 'No input data provided'}, 400
        if errors:
            return errors, 422
        data['email_primary'] = Email(**data['email_primary'])
        contact = Contact(**data)
        db.session.add(contact)
        db.session.commit()
        result = contact_schema.dump(contact).data
        return {"status": 'success', 'data': result}, 201

class ContactOne(Resource):

    def get(self, contact_id):
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 400
        contact = contact_schema.dump(contact).data
        return {'status': 'success', 'data': contact}, 200

    def put(self, contact_id):
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 400
        json_data = request.get_json(force=True)
        data, errors = contact_schema.load(json_data)
        if not data:
            return {'message': 'No input data provided'}, 400
        if errors:
            return errors, 422
        for k,v in data.items():
            setattr(contact, k, v)
        result = contact_schema.dump(exp).data
        return {"status": 'success', 'data': result}, 201
