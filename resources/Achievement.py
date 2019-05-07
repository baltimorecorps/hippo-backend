from flask_restful import Resource, request
from models.achievement_model import Achievement, AchievementSchema
from models.base_model import db

achievement_schema = AchievementSchema()
achievements_schema = AchievementSchema(many=True)


class ContactAchievementAll(Resource):

    def get(self, contact_id):
        achievement = Achievement.query.filter_by(contact_id=contact_id)
        achievement_list = achievements_schema.dump(achievement).data
        return {'status': 'success', 'data': achievement_list}, 200

class ExperienceAchievementAll(Resource):

    def post(self, experience_id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = achievement_schema.load(json_data)
        if errors:
            return errors, 422
        achievement = Achievement(**data)
        db.session.add(achievement)
        db.session.commit()
        result = achievement_schema.dump(achievement).data
        return {"status": 'success', 'data': result}, 201

class AchievementOne(Resource):

    def delete(self, achievement_id):
        achievement = Achievement.query.get(achievement_id)
        if not achievement:
            return {'message': 'Achievement does not exist'}, 400
        db.session.delete(achievement)
        db.session.commit()
        return {"status": 'success'}, 201

    def put(self, achievement_id):
        achievement = Achievement.query.get(achievement_id)
        if not achievement:
            return {'message': 'Achievement does not exist'}, 400
        json_data = request.get_json(force=True)
        # Validate and deserialize input
        data, errors = achievement_schema.load(json_data)
        if not data:
            return {'message': 'No data provided to update'}, 400
        for k,v in data.items():
            setattr(achievement, k, v)
        db.session.commit()
        result = achievement_schema.dump(achievement).data
        return {"status": 'success', 'data': result}, 201
