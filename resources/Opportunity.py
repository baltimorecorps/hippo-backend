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
class OpportunityAll(Resource):
    method_decorators = {
        'post': [login_required, refresh_session],
    }

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




