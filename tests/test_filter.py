import pytest
from pprint import pprint
import json

from models.contact_model import Contact
from models.base_model import db

OUTPUT = {
    'default': [{
        'id': 123,
        'first_name': 'Billy',
        'last_name': 'Daly',
        'email': 'billy@example.com',
        'status': 'approved',
        'phone_primary': '555-245-2351',
        'years_exp': '3-5',
        'job_search_status': 'Actively looking',
        'gender': 'Male',
    }],
    'filter1': [{
        'id': 123,
        'first_name': 'Billy',
        'last_name': 'Daly',
        'email': 'billy@example.com',
        'status': 'approved',
        'phone_primary': '555-245-2351',
        'years_exp': 'filter1',
        'job_search_status': 'filter1',
        'gender': 'Male',
    }],
    'filter2': []
}

QUERIES = {
    'default': {},
    'filter1': {
        'status': ['approved'],
        'years_exp': ['filter1'],
        'job_search_status': ['filter1'],
        'current_job_status': ['filter1'],
        'current_edu_status': ['filter1'],
        'previous_bcorps_program': ['filter1'],
        'hear_about_us': ['filter1']
    },
    'filter2': {
        'years_exp': ['filter2'],
    }
}

UPDATES = {
    'default': None,
    'filter1': {
        'contact': {
            'id': 123,
            'stage': 3
        },
        'profile': {
            'years_exp': 'filter1',
            'job_search_status': 'filter1',
            'current_job_status': 'filter1',
            'current_edu_status': 'filter1',
            'previous_bcorps_program': 'filter1',
            'needs_help_programs': False,
            'hear_about_us': 'filter1',
            'programs_completed': {
                'fellowship': True,
                'public_allies': False,
                'mayoral_fellowship': False,
                'kiva': False,
                'elevation_awards': False,
                'civic_innovators': False
            },
            'roles': {
                'advocacy_public_policy': True,
                'community_engagement_outreach': False,
                'data_analysis': False,
                'fundraising_development': False,
                'program_management': False,
                'marketing_public_relations': False
            }
        },
        'skills': {}
    },
    'filter2': {},
}


@pytest.mark.parametrize(
    "update,query,response",
    [(UPDATES['default'], QUERIES['default'], OUTPUT['default']),
     (UPDATES['filter1'], QUERIES['filter1'], OUTPUT['filter1']),
     (UPDATES['filter2'], QUERIES['filter2'], OUTPUT['filter2'])]
)
def test_basic_filter(app, update, query, response):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    payload = query
    expected = response
    if update:
        contact = Contact.query.get(update['contact']['id'])
        contact.stage = update['contact']['stage']
        contact.profile.update(**update['profile'])
        db.session.commit()

        contact = Contact.query.get(update['contact']['id'])
        assert contact.stage == update['contact']['stage']
        assert contact.profile.years_exp == update['profile']['years_exp']

    with app.test_client() as client:
        response = client.post('/api/contacts/filter',
                               data=json.dumps(payload),
                               headers=headers)

        assert response.status_code == 201

        data = response.json['data']
        print('DATA:')
        pprint(data)
        print('EXPECTED:')
        pprint(expected)
        assert data == expected
