import json
import pytest
import copy
from pprint import pprint

from tests.profile.profile_data import PROFILES_API
from tests.contact.contact_data import INSTRUCTIONS_API

from models.base_model import db
from models.profile_model import Profile
from models.contact_model import Contact
from models.experience_model import Type as ExpType

# imports testing utils
from tests.utils import (
    post_request,
    get_request_one,
    get_request_many,
    put_request,
    delete_request,
    skill_name,
    HEADERS
)


class TestProfileOne:

    def test_get(self, app):
        url = '/api/contacts/123/about-me'
        expected = PROFILES_API['billy']

        get_request_one(app, url, expected)


    def test_get_no_profile(self, app):
        url = '/api/contacts/124/about-me'
        headers = HEADERS

        with app.test_client() as client:
            response = client.get(url , headers=headers)
            assert response.status_code == 404
            assert response.json['message'] == 'Profile does not exist'


    def test_post(self, app):
        url = '/api/contacts/124/about-me/'

        id_, data = post_request(app, url, {})
        contact = Contact.query.get(124)
        assert contact.profile != {}
        pprint(data)
        pprint(PROFILES_API['obama'])
        assert data == PROFILES_API['obama']


    def test_put(self, app):
        url = '/api/contacts/123/about-me'
        update = PROFILES_API['billy_update']
        query = lambda: Profile.query.get(123)
        test = (lambda r: (r.contact.email == 'billy_new@email.com'
                           and r.address_primary.street1 == '124 Main St'
                           and r.race.hispanic == True
                           and r.roles.data_analysis == False
                           and r.race.race_other == 'Test Text'))
        put_request(app, url, update, query, test)


    def test_put_programs_completed_nullable(self, app):
        url = '/api/contacts/123/about-me'
        update = PROFILES_API['billy_null']

        headers = HEADERS

        billy = Contact.query.get(123)
        assert billy.profile.programs_completed is not None

        with app.test_client() as client:
            response = client.put(url, data=json.dumps(update),
                                  headers=headers)
            pprint(response.json)
            assert response.status_code == 200
            billy = Contact.query.get(123)
            assert billy.profile.programs_completed.kiva == False


    def test_put_about_me_race_all(self, app):
        url = '/api/contacts/123/about-me'
        update = PROFILES_API['billy_update']
        query = lambda: Contact.query.get(123)
        test = lambda c: c.race.race_all == 'Hispanic or Latinx;Not Listed;White'

        put_request(app, url, update, query, test)


    def test_put_about_me_race_no_response(self, app):
        url = '/api/contacts/123/about-me'
        query = lambda: Contact.query.get(123)
        test = lambda c: c.race.race_all == 'No Response'
        update = copy.deepcopy(PROFILES_API['billy_update'])
        update['profile']['race'] = {
            'american_indian': False,
            'asian': False,
            'black': False,
            'hispanic': False, # updated
            'hawaiian': False,
            'south_asian': False,
            'white': False,
            'not_listed': False, # updated
            'race_other': None,
        }

        put_request(app, url, update, query, test)


    def test_put_about_me_email(self, app):
        url = '/api/contacts/123/about-me'
        update = PROFILES_API['billy_update']
        query = lambda: Contact.query.get(123)
        test = (lambda c: (c.email == 'billy_new@email.com'
                           and c.email == 'billy_new@email.com'
                           and c.email_main == 'billy_new@email.com'
                           and c.email_primary.email == 'billy_new@email.com'))

        put_request(app, url, update, query, test)


class TestContactInstructions:

    def test_get_completed(self, app):
        url = '/api/contacts/123/instructions'
        expected = INSTRUCTIONS_API['billy']
        get_request_one(app, url, expected)


    def test_get_incomplete(self, app):
        url = '/api/contacts/124/instructions'
        expected = INSTRUCTIONS_API['obama']
        get_request_one(app, url, expected)


    def test_get_instructions_null_question(self, app):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }

        with app.test_client() as client:
            # sets value question to None
            billy = Contact.query.get(123)
            billy.profile.value_question1 = None
            db.session.commit()
            billy = Contact.query.get(123)
            assert billy.profile.value_question1 is None

            response = client.get('/api/contacts/123/instructions',
                                  headers=headers)
            assert response.status_code == 200
            data = json.loads(response.data)['data']
            pprint(data)
            assert data['instructions']['about_me']['is_complete'] == False


    def test_instructions_tag_skills(self, app):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }

        with app.test_client() as client:
            # sets value question to None
            billy = Contact.query.get(123)
            assert billy.tag_skills_complete == True
            for skill in billy.skill_items:
                setattr(skill, 'deleted', True)
            db.session.commit()
            billy = Contact.query.get(123)
            print(billy.skills)
            assert billy.tag_skills_complete == False


    def test_instructions_profile_complete(self, app):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }

        with app.test_client() as client:
            # sets value question to None
            billy = Contact.query.get(123)
            assert billy.add_experience_complete['is_complete'] == True
            assert billy.profile_complete['is_complete'] == True
            for exp in billy.experiences:
                if exp.type == ExpType('Work'):
                    db.session.delete(exp)
            db.session.commit()
            billy = Contact.query.get(123)
            pprint(billy.instructions)
            assert billy.add_experience_complete['is_complete'] == False
            assert billy.profile_complete['is_complete'] == False


    def test_instructions_about_me(self, app):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }
        update = {
            'reset': {
                'gender': None,
                'gender_other': None,
                'pronoun': None,
                'pronoun_other': None,
                'years_exp': None,
                'job_search_status': None,
                'current_job_status': None,
                'current_edu_status': None,
                'previous_bcorps_program': None,
                'value_question1': None,
                'value_question2': None,
                'needs_help_programs': False,
                'hear_about_us': None,
                'hear_about_us_other': None,
            },
            'set': {
                'years_exp': '3-5',
                'job_search_status': 'Test',
                'current_job_status': 'Test',
                'current_edu_status': 'Test',
                'needs_help_programs': True,
                'value_question1': 'Test',
                'value_question2': 'Test'
            }
        }
        with app.test_client() as client:
            # sets value question to None
            profile = Contact.query.get(123).profile
            profile.update(**update['reset'])
            db.session.commit()

            profile = Contact.query.get(123).profile
            assert profile.job_search_status is None
            assert profile.years_exp is None
            assert profile.current_job_status is None
            assert profile.current_edu_status is None

            assert profile.value_alignment_complete == False
            assert profile.interests_and_goals_complete == False
            assert profile.contact.about_me_complete['is_complete'] == False
            profile.update(**update['set'])
            db.session.commit()

            profile = Contact.query.get(123).profile
            assert profile.job_search_status == 'Test'
            assert profile.years_exp == '3-5'
            assert profile.current_job_status == 'Test'
            assert profile.current_edu_status == 'Test'
            assert profile.needs_help_programs == True

            assert profile.value_alignment_complete == True
            assert profile.interests_and_goals_complete == True
            assert profile.contact.about_me_complete['is_complete'] == True


class TestProfileSubmit:
    # TODO: Write test for this outside of trello_integration_test.py
    def test_post(self):
        assert 1
