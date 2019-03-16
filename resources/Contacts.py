from flask_restful import Resource,request
from Model import db, Contact, ContactSchema, Gender, Race

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)


class ContactAll(Resource):
    def get(self):
        data = [
          {
            "id": "1",
            "first_name": "Candy",
            "last_name": "Huber",
            "email": "candyhuber@zounds.com"
          },
          {
            "id": "2",
            "first_name": "Goldie",
            "last_name": "Mcmahon",
            "email": "goldiemcmahon@zounds.com"
          },
          {
            "id": "3",
            "first_name": "Morgan",
            "last_name": "Larson",
            "email": "morganlarson@zounds.com"
          },
          {
            "id": "4",
            "first_name": "Kimberley",
            "last_name": "Cash",
            "email": "kimberleycash@zounds.com"
          },
          {
            "id": "5",
            "first_name": "Stacey",
            "last_name": "Holder",
            "email": "staceyholder@zounds.com"
          },
          {
            "id": "6",
            "first_name": "Benson",
            "last_name": "Alexander",
            "email": "bensonalexander@zounds.com"
          }
        ]
        return data, 200


class ContactOne(Resource):

    def get(self, contact_id):

        contact = {
        "id": 1,
        "first_name": "Benson",
        "last_name": "Alexander",
        "email": "bensonalexander@zounds.com",
        "phone_primary": "401-111-2222",
        "profile_id": 111,
        "gender": "Male",
        "race_all": "Asian",
        "birthdate": "1990-01-02"

        }

        return {'status': 'success', 'data': contact}, 200

    def post(self):
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400

        return {"status": 'success', 'data': json_data}, 201


class Profile(Resource):

    def get(self, contact_id):

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
            },
            {
              "id": "2",
              "host": "Wayfair",
              "title": "Software Engineer",
              "date_start": "2011-01-05",
              "date_end": "2011-04-03",
              "type": "SDE"
            }
          ],
          "education_experiences": [
            {
              "id": "3",
              "host": "Brown University",
              "title": "Student",
              "date_start": "2000-09-05",
              "date_end": "2005-05-03",
              "type": "University"
            }
          ],
          "service_experiences": [
            {
              "id": "4",
              "host": "Happy Tails",
              "title": "Volunteer",
              "date_start": "2001-10-19",
              "date_end": "2002-08-13",
              "type": "NGO"
            }
          ],
          "accomplishments": [
            {
              "host": "Brown University",
              "title": "Academic Excellence Award",
              "date": "2003-05-25",
              "type": "Award"
            }
          ],
          "tags": {
            "function_tags": [
              {
                "id": "1",
                "name": "abc",
                "type": "xyz"
              }
            ],
            "skill_tags": [
              {
                "id": "2",
                "name": "abc",
                "type": "xyz"
              }
            ],
            "topic_tags": [
              {
                "id": "3",
                "name": "abc",
                "type": "xyz"
              }
            ]
          }
        }

        return {'status': 'success', 'data': data}, 200