from flask_restful import Resource, request
from models.achievement_model import Achievement, AchievementSchema
from models.base_model import db

achievement_schema = AchievementSchema()
achievements_schema = AchievementSchema(many=True)


class AchievementAll(Resource):

    def get(self, contact_id):
        achievement = Achievement.query.filter_by(contact_id=contact_id)
        achievement_list = achievements_schema.dump(achievement)
        return {'status': 'success', 'data': achievement_list}, 200
