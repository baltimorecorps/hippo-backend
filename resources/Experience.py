from flask_restful import Resource, request


class ExperienceAll(Resource):

    def get(self, contact_id):

        data = [
            {
                "id": 0,
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidi.",
                "host": "ABC",
                "title": "SDE",
                "date_start": "2014-04-03",
                "date_end": "2015-04-03",
                "type": "education"
            },
            {
                "id": 1,
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidi.",
                "host": "ABC",
                "title": "Accountant",
                "date_start": "2014-04-03",
                "date_end": "2015-04-03",
                "type": "service"
            },
            {
                "id": 2,
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidi.",
                "host": "ABC",
                "title": "Lawyer",
                "date_start": "2014-04-03",
                "date_end": "2015-04-03",
                "type": "work"
            }
        ]
        return {'status': 'success', 'data': data}, 200


class ExperienceOne(Resource):

    def get(self, contact_id, experience_id):
        data = {
                "id": 2,
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididu\
                nt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris\
                 nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit ess\
                 e cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culp\
                 a qui officia deserunt mollit anim id est laborum.",
                "host": "ABC",
                "title": "Lawyer",
                "date_start": "2014-04-03",
                "date_end": "2015-04-03",
                "type": "work"
            }
        return {'status': 'success', 'data': data}, 200


    def post(self, contact_id):
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400

        return {"status": 'success', 'data': json_data}, 201


