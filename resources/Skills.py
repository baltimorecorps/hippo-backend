from flask_restful import Resource, request
from models.contact_model import Contact
from models.skill_model import Skill, SkillSchema
from models.skill_item_model import ContactSkill
from models.base_model import db
from marshmallow import ValidationError

from .skill_utils import (
    get_skill_id, 
    get_or_make_skill, 
    normalize_skill_name, 
    complete_skill,
)

from flask_login import login_required
from auth import (
    refresh_session, 
    is_authorized_view, 
    is_authorized_write, 
    unauthorized
)

skill_schema = SkillSchema()
skills_schema = SkillSchema(many=True)

class AutocompleteSkill(Resource):
    def get(self):
        query = request.args.get('q', '')
        if normalize_skill_name(query) == '':
            result = []
        else:
            result = complete_skill(query)
        return {'status': 'success', 'data': result}, 200

class ContactSkills(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
        'post': [login_required, refresh_session],
    }

    def get(self, contact_id):
        if not is_authorized_view(contact_id): 
            return unauthorized()

        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact not found'}, 404

        skills = skills_schema.dump(contact.skills)
        skills.sort(key=lambda s: s['name'])
        return {'status': 'success', 'data': skills}, 200

    def post(self, contact_id):
        if not is_authorized_write(contact_id): 
            return unauthorized()

        json_data = request.get_json(force=True)
        try:
            data = skill_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422

        if not data:
            return {'message': 'No input data provided'}, 400

        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact not found'}, 404

        name = data['name']
        skill = get_or_make_skill(name)
        contact_skill_names = {s.name for s in contact.skills}
        if name in contact_skill_names:
            result = skill_schema.dump(skill)
            return {'status': 'success', 'data': result}, 200
        else:
            contact.add_skill(skill)
            result = skill_schema.dump(skill)
            return {'status': 'success', 'data': result}, 201

class ContactSkillOne(Resource):
    method_decorators = {
        'delete': [login_required, refresh_session],
    }

    def delete(self, contact_id, skill_id):
        if not is_authorized_write(contact_id): 
            return unauthorized()

        skill = (ContactSkill.query
                 .filter_by(skill_id=skill_id, 
                            contact_id=contact_id)
                 .first())
        if not skill:
            return {'message': 'Skill does not exist'}, 404
        db.session.delete(skill)
        db.session.commit()
        return {'status': 'success'}, 200



