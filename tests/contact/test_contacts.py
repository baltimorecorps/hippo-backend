import json
import pytest
from pprint import pprint

from models.contact_model import Contact, ContactStage
from models.session_model import UserSession

# imports test data
from tests.contact.contact_data import CONTACTS_API, EMAILS_API
from tests.skill.skill_data import CONTACT_SKILLS
from tests.profile.profile_data import PROFILES_API
from tests.program.program_data import PROGRAM_APPS_API

# imports testing utils
from tests.utils import (
    post_request,
    get_request_one,
    get_request_many,
    put_request,
    delete_request
)

CONTACTS = {
    'billy': {
        **CONTACTS_API['billy'],
        'email_primary': EMAILS_API['billy'],
        'skills': CONTACT_SKILLS['billy'],
        'program_apps': PROGRAM_APPS_API['billy']['program_apps'],
        'profile': PROFILES_API['billy']['profile']
    },

    'obama': {
        **CONTACTS_API['obama'],
        'email_primary': EMAILS_API['obama'],
        'skills': CONTACT_SKILLS['obama'],
        'program_apps': [],
        'profile': None
    }
}

POST_PAYLOAD = {
    "first_name": "Tester",
    "last_name": "Byte",
    "email": "testerb@example.com",
    "phone_primary": "111-111-1111",
    "account_id": 'test-valid|0123456789',
    "terms_agreement": True
}

class TestContactAll:

    def test_post(self, app):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype,
            'Authorization': 'Bearer test-valid|0123456789',
        }
        with app.test_client() as client:
            response = client.post('/api/contacts/',
                                   data=json.dumps(POST_PAYLOAD),
                                   headers=headers)
            assert response.status_code == 201
            set_cookie = response.headers.get('set-cookie')
            assert set_cookie is not None
            assert set_cookie.find('HttpOnly;') is not -1
            # Note: Can't test "secure" due to non-https connection
            contact = Contact.query.filter_by(account_id='test-valid|0123456789').first()
            assert contact.first_name == 'Tester'
            assert contact.email == 'testerb@example.com'
            assert contact.profile.years_exp is None
            assert contact.card_id is None

            assert UserSession.query.filter_by(contact_id=contact.id).first()


class TestContactShort:

    def test_get(self, app):

        url = '/api/contacts/'
        expected = [CONTACTS_API['billy'], CONTACTS_API['obama']]

        get_request_many(app, url, expected)

class TestContactAccount:

    def test_get(self):
        assert 1

class TestContactOne:

    def test_get(self):
        assert 1

    def test_put(self):
        assert 1

    def test_delete(self):
        assert 1

class TestContactFull:

    def test_get(self):
        assert 1

class TestContactApproveMany:

    def test_post(self):
        assert 1
