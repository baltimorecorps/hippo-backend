from collections import defaultdict 

from flask_restful import Resource, request
from models.base_model import db
from models.contact_model import Contact
from models.skill_model import (
    Capability, 
    CapabilitySchema, 
    CapabilitySkillSuggestion,
    Skill,
    SkillSchema, 
    SkillRecommendationSchema
)
from models.skill_item_model import ContactSkill
from .Skills import delete_skill
from .skill_utils import get_or_make_skill
from sqlalchemy.sql.expression import and_

capability_schema = CapabilitySchema()
capability_name_schema = CapabilitySchema(only=('id','name'))
skill_schema = SkillSchema()
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

class ContactCapabilitySuggestions(Resource):
    def post(self, contact_id, capability_id):
        json_data = request.get_json(force=True)
        try:
            data = skill_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422

        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404

        capability = Capability.query.get(capability_id)
        if not capability:
            return {'message': 'Capability does not exist'}, 404

        skill = get_or_make_skill(data['name'])
        if skill not in contact.skills:
            contact.add_skill(skill)

        suggestion = CapabilitySkillSuggestion(
            skill_id=skill.id,
            contact_id=contact_id,
            capability_id=capability_id)
        db.session.add(suggestion)
        db.session.commit()

        result = skill_schema.dump(skill)
        return {'status': 'success', 'data': result}, 201


class ContactCapabilitySuggestionOne(Resource):
    def delete(self, contact_id, capability_id, skill_id):
        (result, status_code) = delete_skill(contact_id, skill_id)
        print(result, status_code)
        if status_code != 200:
            return result, status_code
        
        suggestion = CapabilitySkillSuggestion.query.get(
            (contact_id, capability_id, skill_id))
        print(suggestion)
        db.session.delete(suggestion)
        db.session.commit()

        return {'status': 'success'}, 200

# TODO: test
def score_description(description):
    # If we have five or more words, this description is long enough
    if len(description.split()) >= 5:
        return 1
    else:
        return 0

def get_item_achievements(skill_item, capability_id):
    achievement_items = []
    for exp in skill_item.experiences:
        achievement_items.extend(exp.achievements)

    result = {}
    for achievement_item in achievement_items:
        if achievement_item.capability_id == capability_id:
            achievement = achievement_item.achievement
            result[achievement.id] = achievement
    return result

def score_capability(skill_items, capability_id):
    achievements = {}
    for skill_item in skill_items:
        achievements.update(get_item_achievements(skill_item, capability_id))

    score = 0
    for achievement in achievements.values():
        score += score_description(achievement.description)
    return score
        
def get_capability_skill_items(contact_id, capability_id):
    return (ContactSkill.query
            .join(Skill)
            .join(Skill.capabilities)
            .filter(ContactSkill.contact_id == contact_id)
            .filter(Capability.id == capability_id)
            .all())

def get_suggested_skill_items(contact_id, capability_id):
    return (ContactSkill.query
            .join(CapabilitySkillSuggestion,
                  and_(CapabilitySkillSuggestion.contact_id == ContactSkill.contact_id,
                       CapabilitySkillSuggestion.skill_id == ContactSkill.skill_id))
            .filter(ContactSkill.contact_id == contact_id)
            .filter(CapabilitySkillSuggestion.contact_id == contact_id)
            .filter(CapabilitySkillSuggestion.capability_id == capability_id)
            .all())


class ContactCapabilities(Resource):
    def get(self, contact_id):
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404

        other_skill_map = {skill.id: skill for skill in contact.skills}

        cap_results = []
        capabilities = Capability.query.all()
        for capability in capabilities:
            cap = capability_name_schema.dump(capability)
        
            skills = get_capability_skill_items(contact_id, capability.id)
            suggested_skills = get_suggested_skill_items(contact_id, capability.id)

            if not skills and not suggested_skills:
                continue

            # Remove skills that do actually have capabilities
            for skill_item in skills:
                if skill_item.skill_id in other_skill_map:
                    del other_skill_map[skill_item.skill_id]
            for skill_item in suggested_skills:
                if skill_item.skill_id in other_skill_map:
                    del other_skill_map[skill_item.skill_id]

            cap['skills'] = skill_names_schema.dump(
                map(lambda x: x.skill, skills))
            cap['suggested_skills'] = skill_names_schema.dump(
                map(lambda x: x.skill, suggested_skills))
            cap['score'] = score_capability(
                list(skills) + list(suggested_skills), 
                capability.id
            )
            cap_results.append(cap)

        result = {
            'capabilities': cap_results,
            'other_skills': skill_names_schema.dump(other_skill_map.values())
        }
        return {'status': 'success', 'data': result}, 200
