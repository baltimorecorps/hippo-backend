import pytest
from pprint import pprint
import json

from models.contact_model import Contact
from models.base_model import db

from resources.skill_utils import get_contact_skill

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
        'city': 'Baltimore',
        'state': 'Maryland',
        'race': ['No Response']
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
        'city': 'Baltimore',
        'state': 'Maryland',
        'race': ['White']
    }],
    'empty': []
}

QUERIES = {
    'default': {},
    'profile1': {
        'status': ['approved'],
        'years_exp': ['filter1'],
        'job_search_status': ['filter1'],
        'current_job_status': ['filter1'],
        'current_edu_status': ['filter1'],
        'previous_bcorps_program': ['filter1'],
        'hear_about_us': ['filter1']
    },
    'profile2': {'years_exp': ['filter2']},
    'program1': {'programs_completed': {'mayoral_fellowship': True}},
    'program2': {'programs_completed': {'mayoral_fellowship': False}},
    'role1': {'roles': {'advocacy_public_policy': True}},
    'role2': {'roles': {'advocacy_public_policy': True,
                        'community_engagement_outreach': False}},
    'program_app1': {
        'program_apps': [
            {'program': {'name': 'Place for Purpose', 'id': 1},
             'is_interested': True}
        ]
    },
    'program_app2': {
        'program_apps': [
            {'program': {'name': 'Mayoral Fellowship', 'id': 2},
             'is_interested': True}
        ]
    },
    'program_app3': {
        'program_apps': [
            {'program': {'name': 'Place for Purpose', 'id': 1},
             'is_interested': True},
            {'program': {'name': 'Mayoral Fellowship', 'id': 2},
             'is_interested': True}
        ]
    },
    'skills1': {'skills': ['Python', 'Flask']},
    'skills2': {'skills': ['Policy Writing']}
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
            },
            'race': {
                'american_indian': False,
                'asian': False,
                'black': False,
                'hispanic': False,
                'hawaiian': False,
                'south_asian': False,
                'white': True,
                'not_listed': False,
                'race_other': None,
            }
        },
        'skills': {},
        'program_ids': [1, 2]
    },
}


@pytest.mark.parametrize(
    "update,query,response",
    [(UPDATES['default'], QUERIES['default'], OUTPUT['default']),
     (UPDATES['filter1'], QUERIES['profile1'], OUTPUT['filter1']),
     (UPDATES['default'], QUERIES['profile2'], OUTPUT['empty']),
     (UPDATES['default'], QUERIES['program1'], OUTPUT['default']),
     (UPDATES['default'], QUERIES['program2'], OUTPUT['empty']),
     (UPDATES['default'], QUERIES['role1'], OUTPUT['default']),
     (UPDATES['default'], QUERIES['role2'], OUTPUT['empty']),
     (UPDATES['default'], QUERIES['program_app1'], OUTPUT['default']),
     (UPDATES['default'], QUERIES['program_app2'], OUTPUT['empty']),
     (UPDATES['filter1'], QUERIES['program_app3'], OUTPUT['filter1']),
     (UPDATES['default'], QUERIES['skills1'], OUTPUT['default']),
     (UPDATES['default'], QUERIES['skills2'], OUTPUT['empty']),]
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
        for program_app in contact.program_apps:
            if program_app.program_id in update['program_ids']:
                program_app.is_interested = True
        db.session.commit()

        contact = Contact.query.get(update['contact']['id'])
        assert contact.stage == update['contact']['stage']
        assert contact.profile.years_exp == update['profile']['years_exp']
        for program_app in contact.program_apps:
            assert program_app.is_interested == True

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

def test_filter_race_all_null(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    payload = {}
    expected = OUTPUT['default']

    with app.test_client() as client:

        # change race_all to None
        contact = Contact.query.get(123)
        contact.race.race_all = None
        db.session.commit()

        contact = Contact.query.get(123)
        assert contact.race.race_all is None

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


def test_filter_deleted_skill(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    payload = {'skills': ['Python']}
    expected = []

    with app.test_client() as client:

        skill = get_contact_skill(123, 'Python')
        skill.deleted = True
        db.session.commit()

        skill = get_contact_skill(123, 'Python')
        assert skill.deleted == True

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
