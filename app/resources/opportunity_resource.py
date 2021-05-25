import os
import uuid

from flask_restful import Resource, request
from flask_login import login_required
from flask import current_app
from marshmallow import ValidationError

from app.schemas import OpportunitySchema, OpportunityAppSchema
from app.models import (
    db,
    Opportunity,
    Program,
)
from app.auth import (
    refresh_session,
    is_authorized_with_permission,
    unauthorized,
)


def create_new_opportunity(opportunity_data):
    # Make a new random id
    opportunity_data['id'] = str(uuid.uuid4())
    opportunity = Opportunity(**opportunity_data)
    program_name = opportunity_data.get('program_name', None)

    program = Program.query.filter_by(name=program_name).first()
    if program:
        opportunity.program_id = program.id
    else:
        opportunity.program_id = 1

    db.session.add(opportunity)
    db.session.commit()
    return opportunity


opportunity_schema = OpportunitySchema(exclude=['applications'])
opportunities_internal_schema = OpportunitySchema(many=True)
opportunity_org_schema = OpportunitySchema()
opportunities_schema = OpportunitySchema(exclude=['applications'], many=True)


class OpportunityAll(Resource):
    method_decorators = {
        'post': [login_required, refresh_session],
    }

    def get(self):
        opportunities = Opportunity.query.all()
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
        opportunity = create_new_opportunity(data)
        result = opportunity_schema.dump(opportunity)
        return {"status": 'success', 'data': result}, 201


class OpportunityAllInternal(Resource):
    method_decorators = {
        'get': [login_required, refresh_session]
    }

    def get(self):
        opportunities = Opportunity.query.all()
        if not is_authorized_with_permission('view:opportunity-internal'):
            return unauthorized()
        opp_list = opportunities_internal_schema.dump(opportunities)
        return {'status': 'success', 'data': opp_list}, 200


class OpportunityOneOrg(Resource):

    def get(self, opportunity_id):
        opp = Opportunity.query.get(opportunity_id)
        if not opp:
            return {'message': 'Opportunity does not exist'}, 404

        opp_data = opportunity_org_schema.dump(opp)
        return {'status': 'success', 'data': opp_data}, 200


class OpportunityOne(Resource):
    method_decorators = {
        'get': [],
        'put': [login_required, refresh_session],
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

    def put(self, opportunity_id):
        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            return {'message': 'Opportunity does not exist'}, 404

        if not is_authorized_with_permission('write:opportunity'):
            return unauthorized()

        json_data = request.get_json(force=True)
        try:
            data = opportunity_schema.load(json_data, partial=True)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No data provided to update'}, 400

        for k, v in data.items():
            setattr(opportunity, k, v)

        db.session.commit()
        result = opportunity_schema.dump(opportunity)
        return {'status': 'success', 'data': result}, 200


class OpportunityDeactivate(Resource):
    method_decorators = {
        'post': [login_required, refresh_session],
    }

    def post(self, opportunity_id):
        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            return {'message': 'Opportunity does not exist'}, 404

        if not is_authorized_with_permission('write:opportunity'):
            return unauthorized()

        opportunity.is_active = False
        db.session.commit()

        result = opportunity_schema.dump(opportunity)
        return {'status': 'success', 'data': result}, 200


class OpportunityActivate(Resource):
    method_decorators = {
        'post': [login_required, refresh_session],
    }

    def post(self, opportunity_id):
        opportunity = Opportunity.query.get(opportunity_id)
        if not opportunity:
            return {'message': 'Opportunity does not exist'}, 404

        if not is_authorized_with_permission('write:opportunity'):
            return unauthorized()

        opportunity.is_active = True
        db.session.commit()

        result = opportunity_schema.dump(opportunity)
        return {'status': 'success', 'data': result}, 200
