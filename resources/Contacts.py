from flask_restful import Resource, request
from models.contact_model import Contact, ContactSchema, ProfileSchema
from models.email_model import Email
from models.address_model import Address
from models.base_model import db


contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)
profile_schema = ProfileSchema()


class ContactAll(Resource):
    def get(self):
        contacts = Contact.query.all()
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

        # Extract join fields from input if they exist
        emails = []
        addresses = []

        if 'email' in data:
            emails = data.pop('email')
            data['email'] = []

        # if 'email_primary' in data:
        #     email_primary = data.pop('email_primary')
        #     if 'is_primary' in email_primary:
        #         if not email_primary['is_primary']:
        #             return {'message': 'email_primary was set to False, cannot add this email as email_primary'}, 400
        #     email_primary['is_primary'] = True
        #
        #     data['email_primary'] = Email(**email_primary)

        if 'address' in data:
            addresses = data.pop('address')
            data['address'] = []

        contact = Contact(**data)

        # Ensure number of primary emails <= 1
        email_primary_cnt = len([email['is_primary'] for email in emails if 'is_primary' in email and email['is_primary']])
        if email_primary_cnt > 1:
            return {'message': 'Only one email can be set as primary'}, 400

        for email in emails:
            # Create email object and append to contact email field
            contact.email.append(Email(**email))

        # Ensure number of primary addresses <= 1
        address_primary_cnt = len(
            [address['is_primary'] for address in addresses if 'is_primary' in address and addresses['is_primary']])
        if address_primary_cnt > 1:
            return {'message': 'Only one address can be set as primary'}, 400

        for address in addresses:
            # Create address object and append to contact address field
            contact.address.append(Address(**address))

        db.session.add(contact)
        db.session.commit()
        result = contact_schema.dump(contact).data

        return {"status": 'success', 'data': result}, 201


class Profile(Resource):

    def get(self, contact_id):

        contact = Contact.query.filter_by(id=contact_id).first()
        if contact:
            print(profile_schema.dump(contact))
            contact = profile_schema.dump(contact).data
            return {'status': 'success', 'data': contact}, 200
