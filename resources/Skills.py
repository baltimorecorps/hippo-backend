from flask import request as reqobj
from flask_restful import Resource, request
from models.skill_model import SkillItem, SkillItemSchema
from models.base_model import db
from marshmallow import ValidationError

from .skill_utils import get_skill_id

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

        data['id'] = get_skill_id(data['name'])
        data['contact_id'] = contact_id
        skill = SkillItem(**data)
        db.session.add(skill)
        db.session.commit()
        result = skill_schema.dump(skill)
        return {'status': 'success', 'data': result}, 201



