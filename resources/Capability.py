from collections import defaultdict 

from flask_restful import Resource, request
from models.base_model import db
from models.contact_model import Contact
from models.skill_model import (
    Capability, 
    CapabilitySchema, 
    SkillSchema, 
    SkillRecommendationSchema
)

capability_schema = CapabilitySchema()
skill_names_schema = SkillSchema(only=('id', 'name'), many=True)
skill_recs_schema = SkillRecommendationSchema(many=True)
class CapabilityRecommended(Resource):
    def get(self):
        capabilities = Capability.query.all()
        result = []
        for capability in capabilities:
            recs = skill_recs_schema.dump(capability.recommended_skills)
            recs.sort(key=lambda r: r['order'])
            result.append({
                'name': capability.name,
                'skills': recs,
            })

        return {'status': 'success', 'data': result}, 200

class ContactCapabilities(Resource):
    def get(self, contact_id):
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404

        capabilities = {}
        capability_skills = defaultdict(list)
        for skill in contact.skills:
            for capability in skill.capabilities:
                capabilities[capability.id] = capability
                capability_skills[capability.id].append(skill)


        result = []
        for cid, capability in capabilities.items():
            cap_data = capability_schema.dump(capability)
            cap_data['score'] = 0
            cap_data['skills'] = skill_names_schema.dump(capability_skills[cid])
            result.append(cap_data)
        return {'status': 'success', 'data': result}, 200
