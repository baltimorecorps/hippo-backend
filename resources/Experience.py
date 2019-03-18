from flask_restful import Resource, request
from models.experience_model import db, Experience, ExperienceSchema


experience_schema = ExperienceSchema()
experiences_schema = ExperienceSchema(many=True)
class ExperienceAll(Resource):

    def get(self, contact_id):
        experiences = Experience.query.with_entities(Experience.id, Experience.description, Experience.host,
                                                  Experience.title, Experience.date_start, Experience.date_end,
                                                  Experience.type)
        exp_list = experiences_schema.dump(experiences).data

        return {'status': 'success', 'data': exp_list}, 200


class ExperienceOne(Resource):

    def get(self, contact_id, experience_id):
        exp = Experience.query.with_entities(Experience.id, Experience.description, Experience.host,
                                                     Experience.title, Experience.date_start, Experience.date_end,
                                                     Experience.type).filter_by(id=experience_id).first()
        if exp:
            exp_data = experience_schema.dump(exp).data
            return {'status': 'success', 'data': exp_data}, 200


    def post(self, contact_id):
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400

        return {"status": 'success', 'data': json_data}, 201

