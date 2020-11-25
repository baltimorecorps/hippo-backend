import json
import pytest

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

    def test_delete(self):
        assert 1

    def test_put(self):
        assert 1
