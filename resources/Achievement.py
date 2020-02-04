from flask_restful import Resource, request
from models.achievement_model import Achievement, AchievementSchema
from models.base_model import db

from flask_login import login_required
from auth import (
    refresh_session, 
    is_authorized_view,
    unauthorized
)


achievement_schema = AchievementSchema()
achievements_schema = AchievementSchema(many=True)


class AchievementAll(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
    }

    def get(self, contact_id):
        achievement = Achievement.query.filter_by(contact_id=contact_id)
        achievement_list = achievements_schema.dump(achievement)

        if not is_authorized_view(contact_id): 
            return unauthorized()

        return {'status': 'success', 'data': achievement_list}, 200
