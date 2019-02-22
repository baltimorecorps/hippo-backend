from flask_restful import Resource,request
from Model import db, Contact, ContactSchema, Gender, Race

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)


class ContactAll(Resource):
    def get(self):
        contacts = Contact.query.all()
        contacts = contacts_schema.dump(contacts).data
        return {'status': 'success', 'data': contacts}, 200


class ContactOne(Resource):

    def get(self, contact_id):
        contact = Contact.query.filter_by(id=contact_id).first()
        if contact:
            contact = contact_schema.dump(contact).data
            return {'status': 'success', 'data': contact}, 200

    def post(self, contact_id):
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = contact_schema.load(json_data)
        if errors:
            return errors, 422
        contact = Contact.query.filter_by(id=contact_id).first()
        if contact:
            return {'message': 'Contact already exists'}, 400

        contact = Contact(
            id = contact_id,
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

    def put(self, contact_id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = contact_schema.load(json_data)
        if errors:
            return errors, 422

        contact = Contact.query.filter_by(id=contact_id).first()
        if not contact:
            return {'message': 'Contact does not exist'}, 400
        #What fields must we update?
        contact.first_name = data['first_name']
        db.session.commit()

        result = contact_schema.dump(contact).data
        print(result)
        return {"status": 'success', 'data': result}, 204

    def delete(self, contact_id):
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

