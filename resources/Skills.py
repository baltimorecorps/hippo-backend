from flask_restful import Resource, request
from models.skill_model import SkillItem, SkillItemSchema
from models.base_model import db
from marshmallow import ValidationError

from .skill_utils import make_skill, get_skill_id, normalize_skill_name, complete_skill

skill_schema = SkillItemSchema()
skills_schema = SkillItemSchema(many=True)

class AutocompleteSkill(Resource):
    def get(self):
        query = request.args.get('q', '')
        if normalize_skill_name(query) == '':
            result = []
        else:
            result = complete_skill(query)
        return {'status': 'success', 'data': result}, 200

class ContactSkills(Resource):
    def get(self, contact_id):
        skills = (
            SkillItem.query
            .filter_by(contact_id=contact_id)
            .order_by(SkillItem.name)
            .all()
        )
        skills = skills_schema.dump(skills)
        return {'status': 'success', 'data': skills}, 200

    def post(self, contact_id):
        json_data = request.get_json(force=True)
        try:
            data = skill_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422

        if not data:
            return {'message': 'No input data provided'}, 400

        name = data['name']
        id_ = get_skill_id(name)
        skill = SkillItem.query.get((id_, contact_id))
        print(id_, contact_id, skill)
        if not skill:
            skill = make_skill(name, contact_id)
            db.session.add(skill)
            db.session.commit()
            result = skill_schema.dump(skill)
            return {'status': 'success', 'data': result}, 201
        else: 
            result = skill_schema.dump(skill)
            return {'status': 'success', 'data': result}, 200

class ContactSkillOne(Resource):
    def delete(self, contact_id, skill_id):
        skill = SkillItem.query.get((skill_id, contact_id))
        if not skill:
            return {'message': 'Skill does not exist'}, 404
        db.session.delete(skill)
        db.session.commit()
        return {'status': 'success'}, 200


