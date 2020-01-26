from flask_restful import Resource, request
from models.base_model import db

class TalentProgramApp(Resource):

    def post(self):
        form_data = request.form
        return {'status': 'success', 'data': form_data}, 201
