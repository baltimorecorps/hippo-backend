import json
import pytest
from pprint import pprint

from models.contact_model import Contact, ContactStage
from models.session_model import UserSession

# imports test data
from tests.contact.contact_data import CONTACTS_API, INSTRUCTIONS_API, EMAILS_API
from tests.skill.skill_data import CONTACT_SKILLS
from tests.profile.profile_data import PROFILES_API
from tests.program.program_data import PROGRAM_APPS_API
from tests.experience.experience_data import EXPERIENCES_API


# imports testing utils
from tests.utils import (
    post_request,
    get_request_one,
    get_request_many,
    put_request,
    delete_request,
    skill_name
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
    "email_primary": {
        "email": "testerb@example.com",
        "is_primary": True,
    },
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

    def test_post_contact_without_email_primary(self, app):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype,
            'Authorization': 'Bearer test-valid|0123456789',
        }

        payload = POST_PAYLOAD.copy()
        payload['email'] = 'testerb@example.com'
        del payload['email_primary']
        assert payload.get('email_primary', None) is None
        assert payload.get('email') == 'testerb@example.com'

        with app.test_client() as client:
            response = client.post('/api/contacts/',
                                   data=json.dumps(payload),
                                   headers=headers)
            print(response.json)
            assert response.status_code == 201
            contact = Contact.query.filter_by(account_id='test-valid|0123456789').first()
            assert contact.first_name == 'Tester'
            assert contact.email == 'testerb@example.com'
            assert contact.email_primary.email == 'testerb@example.com'

            assert UserSession.query.filter_by(contact_id=contact.id).first()

    def test_post_duplicate_contact(self, app):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype,
            'Authorization': 'Bearer test-valid|0123456789abcdefabcdefff',
        }

        contact_data = POST_PAYLOAD.copy()
        contact_data['account_id'] = 'test-valid|0123456789abcdefabcdefff'

        with app.test_client() as client:
            response = client.post('/api/contacts/',
                                   data=json.dumps(contact_data),
                                   headers=headers)
            assert response.status_code == 400
            message = json.loads(response.data)['message']
            assert message == 'A contact with this account already exists'

class TestContactShort:

    @pytest.mark.parametrize('url', ['/api/contacts/', '/api/contacts/short'])
    def test_get(self, app, url):
        expected = CONTACTS_API.values()
        get_request_many(app, url, expected)

class TestContactAccount:
    # TODO: Write a test for this
    def test_get(self):
        assert 1

class TestContactOne:

    @pytest.mark.parametrize(
        'url,expected',
        [('/api/contacts/123/', CONTACTS['billy'])
        ,('/api/contacts/124/', CONTACTS['obama'])]
    )
    def test_get(self, app, url, expected):
        get_request_one(app, url, expected)


    @pytest.mark.parametrize(
        "url,update,query,test",
        [('/api/contacts/123/',
          {'first_name': 'William', 'last_name':'Daly'},
          lambda: Contact.query.get(123),
          lambda e: e.first_name == 'William',
          ),
         ('/api/contacts/123/',
          {'first_name': 'William', 'programs': 'This should be excluded from load'},
           lambda: Contact.query.get(123),
           lambda e: e.first_name == 'William'
         ),
         ('/api/contacts/123/',
          {'skills': [
              { 'name': 'Python' },
              { 'name': 'Workforce Development' },
          ]},
          lambda: Contact.query.get(123),
          lambda e: (len(e.skills) == 2
                     and sorted(e.skills, key=skill_name)[0].name == 'Python'
                     and sorted(e.skills, key=skill_name)[1].name == 'Workforce Development'),
          )]
    )
    def test_put(self, app, url, update, query, test):
        put_request(app, url, update, query, test)


    def test_delete(self, app):
        url = '/api/contacts/123'
        query = (lambda: Contact.query.get(123))
        delete_request(app, url, query)

class TestContactFull:

    def test_get(self, app):
        url = '/api/contacts/123/profile'
        expected = CONTACTS['billy'].copy()
        expected['experiences'] = [EXPERIENCES_API['billy_edu'],
                                   EXPERIENCES_API['billy_work']]
        expected['instructions'] = INSTRUCTIONS_API['billy']['instructions']
        expected['email'] = expected['email_primary']['email']

        get_request_one(app, url, expected)

class TestContactApproveMany:

    def test_post(self, app):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype,
            'Authorization': 'Bearer test-valid|0123456789',
        }

        expected = [CONTACTS_API['obama'].copy()]
        expected[0]['status'] == 'approved'

        with app.test_client() as client:
            response = client.post('/api/contacts/approve',
                                   data=json.dumps([CONTACTS_API['obama']]),
                                   headers=headers)

            assert response.status_code == 201
            data = json.loads(response.data)['data']
            pprint(data)
            assert len(data) > 0
            for contact in data:
                assert contact['status'] == 'approved'
