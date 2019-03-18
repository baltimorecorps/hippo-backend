from flask_restful import Resource, request
from models.contact_model import Contact, ContactSchema
from models.base_model import db

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)


class ContactAll(Resource):
    def get(self):
        contacts = Contact.query.with_entities(Contact.id, Contact.first_name, Contact.last_name, Contact.email_primary)
        contacts = contacts_schema.dump(contacts).data

        return {'status': 'success', 'data': contacts}, 200


class ContactOne(Resource):

    def get(self, contact_id):

        contact = Contact.query.with_entities(Contact.id, Contact.first_name, Contact.last_name, Contact.email_primary)\
            .filter_by(id=contact_id).first()
        if contact:
            contact = contact_schema.dump(contact).data
            return {'status': 'success', 'data': contact}, 200

    def post(self):
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        data, errors = contact_schema.load(json_data)
        if errors:
            return errors, 422

        contact = Contact(**data)

        db.session.add(contact)
        db.session.commit()
        result = contact_schema.dump(contact).data

        return {"status": 'success', 'data': result}, 201


class Profile(Resource):


    def get(self, contact_id):

        contact = Contact.query.filter_by(id = contact_id).first()
        print(contact)
        if contact:
            contact = contact_schema.dump(contact).data
            return {'status': 'success', 'data': contact}, 200

        data = {
          "id": "1",
          "first_name": "Amy",
          "last_name": "Smith",
          "email_primary": "amy@yahoo.com",
          "phone_primary": "401-234-1124",
          "current_profile": "11",
          "gender": "Female",
          "race_all": "White",
          "birthdate": "1983-02-09",
          "work_experiences": [
            {
              "id": "1",
              "host": "Kayak",
              "title": "Intern",
              "date_start": "2010-05-25",
              "date_end": "2010-12-13",
              "type": "Intern"
            }
          ],
          "service_experiences": [

          ],
          "accomplishments": [

          ]
        }

        return {'status': 'success', 'data': data}, 200