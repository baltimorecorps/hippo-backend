import os

from flask_restful import Resource, request
from flask_login import login_required
from flask import current_app 

from auth import refresh_session

from models.base_model import db

class Opportunity(Resource):
    method_decorators = {
        'post': [login_required, refresh_session],
    }

    def post(self):
        return {'status': 'not implemented'}, 500


