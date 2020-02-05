import os
import uuid

from flask_restful import Resource, request
from flask_login import login_required
from flask import current_app 

from auth import refresh_session

from models.base_model import db
from models.opportunity_model import Opportunity, OpportunitySchema

from auth import is_authorized_with_permission, unauthorized

opportunity_schema = OpportunitySchema()
opportunities_schema = OpportunitySchema(many=True)
class OpportunityAll(Resource):
    method_decorators = {
        'post': [login_required, refresh_session],
    }

    def get(self):
        opportunities = Opportunity.query.all();
        opp_list = opportunities_schema.dump(opportunities)
        return {'status': 'success', 'data': opp_list}, 200

    def post(self):
        json_data = request.get_json(force=True)

        if not is_authorized_with_permission('write:opportunity'):
            return unauthorized()

        try:
            data = opportunity_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422

        # Make a new random id
        data['id'] = str(uuid.uuid4())
        opportunity = Opportunity(**data)

        db.session.add(opportunity)
        db.session.commit()
        result = opportunity_schema.dump(opportunity)
        return {"status": 'success', 'data': result}, 201

class OpportunityOne(Resource):
    method_decorators = {
        'get': [],
        'delete': [login_required, refresh_session],
    }

    def get(self, opportunity_id):
        opp = Opportunity.query.get(opportunity_id)
        if not opp:
            return {'message': 'Opportunity does not exist'}, 404


        opp_data = opportunity_schema.dump(opp)
        return {'status': 'success', 'data': opp_data}, 200

    def delete(self, opportunity_id):

        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            return {'message': 'Opportunity does not exist'}, 404

        if not is_authorized_with_permission('write:opportunity'):
            return unauthorized()

        db.session.delete(opportunity)
        db.session.commit()
        result = opportunity_schema.dump(opportunity)
        return {"status": 'success'}, 200


