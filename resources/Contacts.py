from flask_restful import Resource,request
from Model import db, Contact, ContactSchema, Gender, Race
from flask_sqlalchemy import SQLAlchemy
import json

#db = SQLAlchemy()

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)


class Contacts(Resource):
    def get(self):
        contacts = Contact.query.all()
        contacts = contacts_schema.dump(contacts).data
        return {'status': 'success', 'data': contacts}, 200

    def post(self):
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = contact_schema.load(json_data)
        if errors:
            return errors, 422
        contact = Contact.query.filter_by(first_name=data['first_name']).first()
        if contact:
            return {'message': 'Contact already exists'}, 400

        contact = Contact(
            first_name=json_data['first_name'],
            last_name =json_data['last_name'],
            email_primary=json_data['email_primary'],
            phone_primary=json_data['phone_primary'],
            current_profile=json_data['current_profile'],
            gender=Gender(json_data['gender']),
            race_all=Race(json_data['race_all']),
            birthdate=json_data['birthdate']
        )

        db.session.add(contact)
        db.session.commit()

        result = contact_schema.dump(contact).data

        return {"status": 'success', 'data': result}, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = contact_schema.load(json_data)
        if errors:
            return errors, 422
        contact = Contact.query.filter_by(id=data['id'])
        print(contact)
        if not contact:
            return {'message': 'Contact does not exist'}, 400
        contact.first_name = data['first_name']
        db.session.commit()

        result = contact_schema.dump(contact).data

        return {"status": 'success', 'data': result}, 204

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = contact_schema.load(json_data)
        if errors:
            return errors, 422
        contact = Contact.query.filter_by(id=data['id']).delete()
        if not contact:
            return {'message': 'Contact does not exist'}, 400
        db.session.commit()

        result = contact_schema.dump(contact).data

        return {"status": 'success', 'data': result}, 204

