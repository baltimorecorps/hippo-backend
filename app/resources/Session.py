import os
from datetime import datetime, timedelta
from urllib.request import urlopen
from functools import wraps

from flask_restful import Resource, request
from flask_login import current_user, login_required, login_user, logout_user
from flask import current_app 

from app.auth import validate_jwt, create_session, delete_session, refresh_session
from app.models.base_model import db
from app.models.session_model import UserSessionSchema
from app.models.contact_model import Contact

session_schema = UserSessionSchema()
class Session(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
        'post': [validate_jwt],
        'delete': [login_required],
    }

    def get(self):
        result = session_schema.dump(current_user)
        return {'status': 'success', 'data': result }, 200

    def post(self):
        account_id = request.jwt['sub']
        contact = Contact.query.filter_by(account_id=account_id).first()
        if not contact:
            return {'message': 'Contact does not exist for that account'}, 400

        user_session = create_session(contact.id, request.jwt)
        login_user(user_session)
        
        result = session_schema.dump(user_session)
        return {'status': 'success', 'data': result}, 201

    def delete(self):
        delete_session(current_user)
        logout_user()


