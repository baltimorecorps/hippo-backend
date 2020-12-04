from tests.contact.contact_data import CONTACTS_API

PROGRAMS_DATABASE = {
    'pfp': {
        'id': 1,
        'name': 'Place for Purpose'
    },
    'mayoral': {
        'id': 2,
        'name': 'Mayoral Fellowship'
    },
}

PROGRAM_APPS_DATABASE = {
    'billy_pfp': {
        'id': 7,
        'is_interested': True,
        'is_approved': True,
        'decision_date': '2020-01-01',
    },
    'billy_mayoral': {
        'id': 8,
        'is_interested': False,
        'is_approved': False,
        'decision_date': None,
    },
    'obama_pfp': {
        'id': 1,
        'is_interested': True,
        'is_approved': False,
        'decision_date': None,
    },
    'obama_mayoral': {
        'id': 2,
        'is_interested': False,
        'is_approved': False,
        'decision_date': None,
    }
}

PROGRAMS_API = PROGRAMS_DATABASE

PROGRAM_APPS_API = {
    'billy': {
        **CONTACTS_API['billy'],
        'program_apps': [
            {**PROGRAM_APPS_DATABASE['billy_pfp'],
             'program': PROGRAMS_API['pfp'],
             'status': 'Eligible'},
            {**PROGRAM_APPS_DATABASE['billy_mayoral'],
             'program': PROGRAMS_API['mayoral'],
             'status': 'Not interested'},
        ]},
    'obama': {
        **CONTACTS_API['obama'],
        'program_apps': [
            {**PROGRAM_APPS_DATABASE['obama_pfp'],
             'program': PROGRAMS_API['pfp'],
             'status': 'Waiting for approval'},
            {**PROGRAM_APPS_DATABASE['obama_mayoral'],
             'program': PROGRAMS_API['mayoral'],
             'status': 'Not interested'},
        ]},
    'obama_none': {
        **CONTACTS_API['obama'],
        'program_apps': []}
}
