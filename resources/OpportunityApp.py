import os
import uuid

from flask_restful import Resource, request
from flask_login import login_required

from models.base_model import db

from auth import (
    is_authorized_view, 
    is_authorized_write, 
    unauthorized, 
    refresh_session
)
from models.opportunity_app_model import OpportunityApp, OpportunityAppSchema, ApplicationStage

opportunity_app_schema = OpportunityAppSchema()

class OpportunityAppOne(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
        'post': [login_required, refresh_session],
        'put': [login_required, refresh_session],
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

    def post(self, contact_id, opportunity_id):
        if not is_authorized_write(contact_id):
            return unauthorized()

        opportunity_app = (OpportunityApp.query
            .filter_by(contact_id=contact_id, opportunity_id=opportunity_id)
            .first())

        if opportunity_app:
            return {'message': 'Application already exists!'}, 400

        opportunity_app = OpportunityApp(
            id=str(uuid.uuid4()),
            contact_id=contact_id,
            opportunity_id=opportunity_id,
            interest_statement=''
        )
        db.session.add(opportunity_app)
        db.session.commit()

        data = opportunity_app_schema.dump(opportunity_app)
        return {'status': 'success', 'data': data}, 201

    def put(self, contact_id, opportunity_id):
        if not is_authorized_write(contact_id):
            return unauthorized()

        json_data = request.get_json(force=True)
        try:
            data = opportunity_app_schema.load(json_data, partial=True)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No data provided to update'}, 400

        opportunity_app = (OpportunityApp.query
            .filter_by(contact_id=contact_id, opportunity_id=opportunity_id)
            .first())

        if not opportunity_app:
            return {'message': 'Application does not exist'}, 404

        for k,v in data.items():
            setattr(opportunity_app, k, v)

        db.session.commit()
        result = opportunity_app_schema.dump(opportunity_app)
        return {'status': 'success', 'data': result}, 200
        
class OpportunityAppSubmit(Resource):
    method_decorators = {
        'post': [login_required, refresh_session],
    }

    def post(self, contact_id, opportunity_id):
        if not is_authorized_write(contact_id):
            return unauthorized()

        opportunity_app = (OpportunityApp.query
            .filter_by(contact_id=contact_id, opportunity_id=opportunity_id)
            .first())

        if not opportunity_app:
            return {'message': 'Application does not exist'}, 404
        if opportunity_app.stage >= ApplicationStage.submitted.value:
            return {'message': 'Application is already submitted'}, 400

        opportunity_app.stage = ApplicationStage.submitted.value
        db.session.commit()
        result = opportunity_app_schema.dump(opportunity_app)
        return {'status': 'success', 'data': result}, 200
     



