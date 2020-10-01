from flask_restful import Resource, request
from models.experience_model import Experience, ExperienceSchema, Type
from models.achievement_model import Achievement, AchievementSchema
from models.base_model import db
import datetime as dt
from operator import attrgetter
from marshmallow import ValidationError

from models.skill_model import Skill, Capability
from .skill_utils import get_skill_id, get_or_make_skill

from flask_login import login_required
from auth import (
    refresh_session,
    is_authorized_view,
    is_authorized_write,
    unauthorized
)



experience_schema = ExperienceSchema()
experiences_schema = ExperienceSchema(many=True)
type_list = [m for m in Type.__members__.keys()]

def add_achievements(achievements, experience):
    for achievement in achievements:
        a = Achievement(description=achievement['description'])
        if 'id' in achievement:
            a.id = achievement['id']
        a.contact = experience.contact
        a.experience = experience
        if 'skills' in achievement:
            for skill in achievement['skills']:
                capability = None
                if skill.get('capability_id') is not None:
                    capability = Capability.query.get(skill['capability_id'])

                a.add_skill(get_or_make_skill(skill['name']), capability)
        db.session.add(a)

def add_skills(skills, experience):
    for skill_data in skills:
        skill = get_or_make_skill(skill_data['name'])
        experience.add_skill(skill)

def sync_skills(skills, experience):
    print(skills)
    add_skills(skills, experience)

    current_skills = {s['name'] for s in skills}
    for skill_item in experience.skill_items:
        if skill_item.skill.name not in current_skills:
            skill_item.deleted = True



class ExperienceAll(Resource):
    method_decorators = {
        'get': [], # used to be [login_required, refresh_session]
        'post': [login_required, refresh_session],
    }

    def get(self, contact_id):
        """Returns all of the experiences associated with a given contact

        ENDPOINT
            - POST api/contacts/<int:contact_id>/experiences

        PATH PARAMETERS
            - contact_id: (int) primary key of row in contact table

        QUERY PARAMETERS
            - type
                - work: Includes internships, paid employment, etc.
                - education: Includes degrees, courses, certificates, etc.
                - accomplishment: Includes honors, work products, portolio, etc.

        RESPONSE BODY
            [{'id': 511,
            'contact_id': 124,
            'description': 'Test description',
            'host': 'Columbia University',
            'title': 'Political Science',
            'degree': None,
            'degree_other': None,
            'link': 'www.google.com',
            'link_name': 'Google',
            'start_year': 1979,
            'end_year': 1983,
            'location': 'New York, NY, USA',
            'type': 'Accomplishment',
            'end_month': 'May',
            'start_month': 'September',
            'length_year': 3,
            'length_month': 8,
            'is_current': False,
            'achievements': [
                {'id': 81,
                'description': 'Redesigned the salesforce...',
                'skills': [{'name': 'Python','capability_id': 'cap:it'}]}
            ]},
            {...}]

        RESPONSE STATUS CODES
            - 201: Success
            - 422: Error validating payload
            - 400: No input data provided OR Account does not match post

        MODELS
            - Contact
            - Email
        """
        # TODO: Create employer permissions so we can restore AuthZ
        #if not is_authorized_view(contact_id):
        #    return unauthorized()

        type_arg = request.args.get('type')
        if type_arg:
            if type_arg not in Type.__members__:
                return {'message':
                        f'No such experience type, '
                        f'choose an option from this list: {type_list}'}, 400
            exp = (Experience.query.filter_by(contact_id=contact_id,
                                              type=Type[type_arg]))
        else:
            exp = (Experience.query.filter_by(contact_id=contact_id))
        exp_sorted = sorted(exp,
                            key=attrgetter('date_end', 'date_start'),
                            reverse=True)
        exp_list = experiences_schema.dump(exp_sorted)
        return {'status': 'success', 'data': exp_list}, 200

    def post(self, contact_id):
        if not is_authorized_write(contact_id):
            return unauthorized()

        json_data = request.get_json(force=True)
        try:
            data = experience_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No data provided to update'}, 400

        #pull out the achievements to create them later
        achievements = data.pop('achievements', None)
        skills = data.pop('skills', None)

        #create the experience record
        exp = Experience(**data)
        db.session.add(exp)
        db.session.commit()

        # Need to add after the first commit so that we have a reference to
        # our 'Contact' object
        if skills:
            add_skills(skills, exp)

        if achievements:
            add_achievements(achievements, exp)
        db.session.commit()

        result = experience_schema.dump(exp)
        return {"status": 'success', 'data': result}, 201

class ExperienceOne(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
        'delete': [login_required, refresh_session],
        'put': [login_required, refresh_session],
    }

    def get(self, experience_id):
        exp = Experience.query.get(experience_id)
        if not exp:
            return {'message': 'Experience does not exist'}, 404

        if not is_authorized_view(exp.contact.id):
            return unauthorized()

        exp_data = experience_schema.dump(exp)
        return {'status': 'success', 'data': exp_data}, 200

    def delete(self, experience_id):
        exp = Experience.query.get(experience_id)
        if not exp:
            return {'message': 'Experience does not exist'}, 404

        if not is_authorized_write(exp.contact.id):
            return unauthorized()

        db.session.delete(exp)
        db.session.commit()
        return {"status": 'success'}, 200

    def put(self, experience_id):
        exp = Experience.query.get(experience_id)
        if not exp:
            return {'message': 'Experience does not exist'}, 404

        if not is_authorized_write(exp.contact.id):
            return unauthorized()

        json_data = request.get_json(force=True)
        try:
            data = experience_schema.load(json_data, partial=True)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No data provided to update'}, 400

        achievements = data.pop('achievements', None)
        skills = data.pop('skills', None)

        for k,v in data.items():
            setattr(exp, k, v)

        # This has to come before updaing achievements, otherwise deleting a
        # skill here could wipe out an achievement skill that was just added
        if skills is not None:
            sync_skills(skills, exp)

        if achievements is not None:
            del exp.achievements[:]
            add_achievements(achievements, exp)


        db.session.commit()
        result = experience_schema.dump(exp)
        return {'status': 'success', 'data': result}, 200
