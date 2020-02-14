from flask_restful import Resource, request
from models.base_model import db
from models.skill_model import Capability, SkillRecommendationSchema

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
