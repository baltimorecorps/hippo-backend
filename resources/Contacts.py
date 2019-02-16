from flask_restful import Resource,request
from Model import Contact, ContactSchema
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)


class Contacts(Resource):
    def get(self):
        contacts = Contact.query.all()
        contacts = contacts_schema.dump(contacts).data
        return {'status':'success', 'data': contacts}, 200

    # def post(self):
    #     json_data = request.get_json(force=True)
    #
    #     if not json_data:
    #         return {'message': 'No input data provided'}, 400
    #     # Validate and deserialize input
    #     data, errors = contact_schema.load(json_data)
    #     if errors:
    #         return errors, 422
    #     contact = Contact.query.filter_by(first_name=data['first_name']).first()
    #     if contact:
    #         return {'message': 'Contact already exists'}, 400
    #     contact = contact_schema.dump(json_data)
    #
    #     db.session.add(contact)
    #     db.session.commit()
    #
    #     result = contact_schema.dump(contact).data
    #
    #     return {"status": 'success', 'data': json_data}, 201


