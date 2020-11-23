import json
import pytest
import copy
from pprint import pprint

from tests.profile.profile_data import PROFILES_API

from models.profile_model import Profile
from models.contact_model import Contact

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


    def test_post(self):
        assert 1

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


class TestContactInstructions:

    def test_get(self):
        assert 1


class TestProfileSubmit:

    def test_post(self):
        assert 1
