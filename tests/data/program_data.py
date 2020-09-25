from .contact_data import CONTACTS_API

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

PROGRAM_CONTACTS_DATABASE = {
    'billy_pfp': {
        'id': 5,
        'contact_id': 123,
        'card_id': None,
        'stage': 1,
        'is_active': True,
        'is_approved': True,
    },
    'obama_pfp': {
        'id': 6,
        'contact_id': 124,
        'card_id': 'card',
        'stage': 1,
        'is_active': True,
        'is_approved': False,
    },
    'billy_mayoral': {
        'id': 7,
        'contact_id': 123,
        'card_id': 'card',
        'stage': 1,
        'is_active': True,
        'is_approved': False,
    }
}

PROGRAMS_API = PROGRAMS_DATABASE

PROGRAM_CONTACTS_API = {
    'billy_pfp': {
        **PROGRAM_CONTACTS_DATABASE['billy_pfp'],
        'program': PROGRAMS_API['pfp']
    },
    'obama_pfp': {
        **PROGRAM_CONTACTS_DATABASE['obama_pfp'],
        'program': PROGRAMS_API['pfp'],
    },
    'billy_mayoral': {
        **PROGRAM_CONTACTS_DATABASE['billy_mayoral'],
        'program': PROGRAMS_API['mayoral'],
    }
}

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
