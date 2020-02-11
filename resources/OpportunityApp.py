import os
import uuid

from flask_restful import Resource, request
from flask_login import login_required

from models.base_model import db

from auth import is_authorized_view, unauthorized, refresh_session
from models.opportunity_app_model import OpportunityApp, OpportunityAppSchema

opportunity_app_schema = OpportunityAppSchema()

class OpportunityAppOne(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
    }

    def get(self, contact_id, opportunity_id):
        if not is_authorized_view(contact_id):
            return unauthorized()

        opportunity_app = (OpportunityApp.query
            .filter_by(contact_id=contact_id, opportunity_id=opportunity_id)
            .first())

        if not opportunity_app:
            return {'message': 'Application does not exist'}, 404
        

        data = opportunity_app_schema.dump(opportunity_app)
        return {'status': 'success', 'data': data}, 200


