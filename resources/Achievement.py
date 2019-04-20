from flask_restful import Resource, request
from models.achievement_model import Achievement, AchievementSchema
from models.base_model import db

achievement_schema = AchievementSchema()


class AchievementsAll(Resource):

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
        achievement = Achievement.query.filter_by(id=achievement_id)
        if not achievement.first():
            return {'message': 'Achievement does not exist'}, 400
        achievement.delete()
        db.session.commit()
        return {"status": 'success'}, 201

    def put(self, achievement_id):
        achievement = Achievement.query.filter_by(id=achievement_id)
        if not achievement.first():
            return {'message': 'Achievement does not exist'}, 400
        json_data = request.get_json(force=True)
        # Validate and deserialize input
        data, errors = achievement_schema.load(json_data)
        if not data:
            return {'message': 'No data provided to update'}, 400

        # ach = Achievement(**data)
        achievement.update(data)
        db.session.commit()
        return {"status": 'success'}, 201
