import json
import pytest
from pprint import pprint


from models.base_model import db
from models.experience_model import Experience, Month, Type as ExpType
from models.skill_item_model import (
    ContactSkill,
    ExperienceSkill,
    AchievementSkill,
)

# imports testing utils
from tests.utils import (
    post_request,
    get_request_one,
    get_request_many,
    put_request,
    delete_request,
    skill_name
)

#imports test data
from tests.experience.experience_data import EXPERIENCES_API, ACHIEVEMENTS_API

POSTS={'experience': {
        'description': 'Test description',
        'host': 'Test Org',
        'title': 'Test title',
        'start_month': 'September',
        'start_year': 2000,
        'end_month': 'May',
        'end_year': 2019,
        'link': None,
        'link_name': None,
        'type': 'Work',
        'contact_id': 123,
        'location': 'Test City, MD, USA',
        'achievements': [
            {'description': 'Test achievement 1'},
            {'description': 'Test achievement 2', 'skills': [
                { 'name': 'Community Organizing', 'capability_id': 'cap:advocacy' },
                { 'name': 'Test Skill 1' }
            ]},
        ],
    }}

class TestExperienceAll:

    def test_get(self):
        assert 1

    @pytest.mark.parametrize(
        "url,data,query",
        [('/api/contacts/123/experiences/',
        POSTS['experience'],
        lambda id: Experience.query.get(id)
        )])

    def test_post(self, app, url, data, query):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }

        id_, _ = post_request(app, url, data)
        assert query(id_) is not None


class TestExperienceOne:

    def test_get(self):
        assert 1

    def test_post_experience_date(self, app):
        id_, _ = post_request(app, '/api/contacts/123/experiences/',
                            POSTS['experience'])
        assert Experience.query.get(id_).end_month == Month.may
        assert Experience.query.get(id_).end_year == 2019
        assert Experience.query.get(id_).start_month == Month.september
        assert Experience.query.get(id_).start_year == 2000


    def test_post_experience_null_start_date(self, app):
        exp = POSTS['experience'].copy()
        exp['start_month'] = 'none'
        exp['start_year'] = 0
        id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
        assert Experience.query.get(id_) is not None
        assert Experience.query.get(id_).start_month == Month.none
        assert Experience.query.get(id_).start_year == 0
        pprint(Experience.query.get(id_).start_month)
        pprint(Experience.query.get(id_).start_year)

    def test_post_experience_current(self, app):
        exp = POSTS['experience'].copy()
        exp['end_month'] = 'none'
        exp['end_year'] = 0
        id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
        assert Experience.query.get(id_) is not None
        assert Experience.query.get(id_).is_current == True

    def test_post_experience_dump_only(self, app):
        exp = POSTS['experience'].copy()
        exp['length_year'] = 18
        exp['length_month'] = 8
        exp['is_current'] = False
        exp['id'] = 1
        id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
        assert Experience.query.get(id_) is not None

    def test_post_experience_skills(self, app):
        exp = POSTS['experience'].copy()
        exp['skills'] = [{'name': 'C++'}, {'name': 'Python'}]
        id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
        assert Experience.query.get(id_).skills[0].name == 'C++'
        assert Experience.query.get(id_).skills[1].name == 'Community Organizing'
        assert Experience.query.get(id_).skills[2].name == 'Python'
        assert Experience.query.get(id_).skills[3].name == 'Test Skill 1'

    def test_post_experience_achievement_skills(self, app):
        exp = POSTS['experience']
        id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
        skills = Experience.query.get(id_).achievements[1].skills
        assert len(Experience.query.get(id_).achievements[1].skills) == 2
        assert skills[0]['name'] == 'Community Organizing'
        assert skills[0]['capability_id'] == 'cap:advocacy'
        assert skills[1]['name'] == 'Test Skill 1'
        assert skills[1]['capability_id'] is None

    def test_delete(self):
        assert 1

    def test_put(self):
        assert 1
