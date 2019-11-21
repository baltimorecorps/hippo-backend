from flask import request as reqobj
from flask_restful import Resource, request
from models.skill_model import SkillItem, SkillItemSchema
from models.base_model import db
from marshmallow import ValidationError

from .skill_utils import make_skill

skill_schema = SkillItemSchema()
skills_schema = SkillItemSchema(many=True)

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

        skill = make_skill(data['name'], contact_id)
        db.session.add(skill)
        db.session.commit()
        result = skill_schema.dump(skill)
        return {'status': 'success', 'data': result}, 201

class ContactSkillOne(Resource):
    def delete(self, contact_id, skill_id):
        skill = SkillItem.query.get((skill_id, contact_id))
        if not skill:
            return {'message': 'Skill does not exist'}, 404
        db.session.delete(skill)
        db.session.commit()
        return {'status': 'success'}, 200



