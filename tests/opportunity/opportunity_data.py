import copy

from tests.contact.contact_data import CONTACTS_API

RESUME_SNAPSHOTS = {
    'snapshot1': {'id': 111, 'resume': '{"test": "snapshot1"}'}
}

OPPS_DATABASE = {
    'opp1': {
        'id': '123abc',
        'title': "Test Opportunity",
        'short_description': "This is a test opportunity.",
        'gdoc_link': "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        'org_name': 'Test Org',
        'program_id': 1,
        'is_active': True,
        'program_name': "Place for Purpose"
    },
    'opp2': {
        'id': '222abc',
        'title': "Another Test Opportunity",
        'short_description': "This is another test opportunity.",
        'gdoc_link': "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        'org_name': 'Test Org',
        'program_id': 2,
        'is_active': True,
        'program_name': "Mayoral Fellowship"
    },
    'opp3': {
        'id': '333abc',
        'title': "A Third Test Opportunity",
        'short_description': "This is another test opportunity.",
        'gdoc_link': "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        'org_name': 'Test Org',
        'program_id': 1,
        'is_active': True,
        'program_name': "Place for Purpose"
    },
}

OPP_APPS_DATABASE = {
    'billy1': {
        'id': 'a1',
        'interest_statement': "I'm interested in this test opportunity",
        'is_active': True,
        'interview_date': None,
        'interview_time': None,
    },
    'billy2': {
        'id': 'a2',
        'interest_statement': "I'm also interested in this test opportunity",
        'is_active': True,
        'interview_date': None,
        'interview_time': None,
    },
    'obama1': {
        'id': 'a3',
        'interest_statement': "I'm also interested in this test opportunity",
        'is_active': True,
        'interview_date': None,
        'interview_time': None,
    }
}


OPPS_API = {
    'opp1': {**OPPS_DATABASE['opp1'], 'status': 'submitted'},
    'opp2': {**OPPS_DATABASE['opp2'], 'status': 'submitted'},
    'opp3': {**OPPS_DATABASE['opp3'], 'status': 'submitted'},
}

OPP_APPS_API = {
    'billy1': {
        **OPP_APPS_DATABASE['billy1'],
        'contact': CONTACTS_API['billy'],
        'opportunity': OPPS_API['opp1'],
        'resume': {'test': 'snapshot1'},
        'status': 'submitted',
        'interview_completed': False,

    },
    'billy2': {
        **OPP_APPS_DATABASE['billy2'],
        'contact': CONTACTS_API['billy'],
        'opportunity': OPPS_API['opp2'],
        'resume': None,
        'status': 'draft',
        'interview_completed': False
    },
    'obama1': {
        **OPP_APPS_DATABASE['obama1'],
        'contact': CONTACTS_API['obama'],
        'opportunity': OPPS_API['opp1'],
        'resume': None,
        'status': 'recommended',
        'interview_completed': False
    }
}
billy_update = copy.deepcopy(OPP_APPS_API['billy1'])
billy_update['interest_statement'] = 'dfdddsdfff'
OPP_APPS_API['billy_update'] = billy_update


OPPS_INTERNAL_API = {
    'opp1': {**OPPS_API['opp1'],
             'applications': [OPP_APPS_API['billy1'].copy(),
                              OPP_APPS_API['obama1'].copy()]},
    'opp2': {**OPPS_API['opp2'],
             'applications': [OPP_APPS_API['billy2'].copy()]},
    'opp3': {**OPPS_API['opp3'],
             'applications': []},
}
# this deletes the opportunity field from each application
del OPPS_INTERNAL_API['opp1']['applications'][0]['opportunity']
del OPPS_INTERNAL_API['opp1']['applications'][1]['opportunity']
del OPPS_INTERNAL_API['opp2']['applications'][0]['opportunity']

del OPPS_INTERNAL_API['opp1']['applications'][0]['resume']
del OPPS_INTERNAL_API['opp1']['applications'][1]['resume']
del OPPS_INTERNAL_API['opp2']['applications'][0]['resume']
