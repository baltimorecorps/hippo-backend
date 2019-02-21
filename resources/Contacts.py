from flask_restful import Resource,request
from Model import Contact, ContactSchema, Gender, Race
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

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

        # print(contact.first_name, type(contact.first_name))
        # print(contact.last_name, type(contact.last_name))
        # print(contact.email_primary, type(contact.email_primary))
        # print(contact.phone_primary, type(contact.phone_primary))
        # print(contact.current_profile, type(contact.current_profile))
        # print(contact.gender, type(contact.gender))
        # print(contact.race_all, type(contact.race_all))
        # print(contact.birthdate, type(contact.birthdate))

        # db.session.add(Contact(id=223, first_name='amsa', last_name='arq', email_primary='s1@cv.com',
        #                        phone_primary='3455323', current_profile=213, gender='Male', race_all='Asian',
        #                        birthdate='2012-04-23'))

        # db.session.add("INSERT INTO contact (id, first_name, last_name, email_primary, phone_primary, current_profile, gender, "\
        #                "race_all, birthdate) VALUES (223, 'amsa', 'arq', 's1@cv.com', '3455323', 213, 'Male', 'Asian', 2012-04-23)")
        db.session.add(contact)
        db.session.commit()


        #result = contact_schema.dump(contact).data

        return {"status": 'success', 'data': json_data}, 201

