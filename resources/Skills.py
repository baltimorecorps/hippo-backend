from flask import request as reqobj
from flask_restful import Resource, request
from models.skill_model import SkillItem, SkillItemSchema
from marshmallow import ValidationError

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

