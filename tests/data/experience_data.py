# from .skill_data import SKILLS_API

import datetime as dt
import math

ACHIEVEMENTS_DATABASE = {
    'billy_work1': {
        'id': 81,
        'description': 'Redesigned the Salesforce architecture to facilitate easier reporting.',
    },
    'billy_work2': {
        'id': 82,
        'description': 'Formalized organizational strategy for defining and analyzing KPIs.',
    },
    'billy_work3': {
        'id': 83,
        'description': 'Developed recruitment projection tools to model and track progress to goals.',
    },
    'billy_edu1': {
        'id': 84,
        'description': 'Did some stuff',
    }
}

DATE_START = dt.date(2000, 1, 1)
DATE_END = dt.datetime.today()
DATE_LENGTH = ((DATE_END.year - DATE_START.year) * 12
               + DATE_END.month - DATE_START.month)

EXPERIENCES_DATABASE = {
    'obama_portfolio': {
        'id': 511,
        'contact_id': 124,
        'description': 'Test description',
        'host': 'Columbia University',
        'title': 'Political Science',
        'degree': None,
        'degree_other': None,
        'link': 'www.google.com',
        'link_name': 'Google',
        'start_year': 1979,
        'end_year': 1983,
        'location': 'New York, NY, USA',
    },
    'billy_edu': {
        'id': 512,
        'contact_id': 123,
        'description': None,
        'host': 'Goucher College',
        'title': 'Economics',
        'degree': 'Undergraduate',
        'degree_other': 'Study Abroad',
        'link': None,
        'link_name': None,
        'start_year': 2012,
        'end_year': 2016,
        'location': 'Towson, MD, USA',
    },
    'billy_work' : {
        'id': 513,
        'contact_id': 123,
        'description': 'Test description here',
        'host': 'Baltimore Corps',
        'title': 'Systems Design Manager',
        'degree': None,
        'degree_other': None,
        'link': None,
        'link_name': None,
        'start_year': 2000,
        'end_year': 0,
        'location': 'Baltimore, MD, USA',
    },
}

ACHIEVEMENTS_API = {
    'billy_work': [
        {
            **ACHIEVEMENTS_DATABASE['billy_work1'],
            'skills': [{
                'name': 'Flask','capability_id': 'cap:it'
            }]
        },
        {
            **ACHIEVEMENTS_DATABASE['billy_work2'],
            'skills': [{
                'name': 'Community Organizing', 'capability_id': 'cap:advocacy'
            }]
        },
        {
            **ACHIEVEMENTS_DATABASE['billy_work3'],
            'skills': [{
                'name': 'Web Development', 'capability_id': 'cap:it',
            }]
        }
    ],
    'billy_edu': [{
            **ACHIEVEMENTS_DATABASE['billy_edu1'],
            'skills': [{
                'name': 'Python', 'capability_id': 'cap:it',
            }],
        }
    ]
}

EXPERIENCES_API ={
    'obama_portfolio': {
        **EXPERIENCES_DATABASE['obama_portfolio'],
        'type': 'Accomplishment',
        'end_month': 'May',
        'start_month': 'September',
        'is_current': False,
        'length_year': 3,
        'length_month': 8,
        'achievements': [],
        'skills': [],
    },
    'billy_edu': {
        **EXPERIENCES_DATABASE['billy_edu'],
        'type': 'Education',
        'start_month': 'September',
        'end_month': 'May',
        'length_year': 3,
        'length_month': 8,
        'is_current': False,
        'achievements': ACHIEVEMENTS_API['billy_edu'],
        'skills': [],
    },
    'billy_work': {
        **EXPERIENCES_DATABASE['billy_work'],
        'type': 'Work',
        'start_month': 'January',
        'end_month': 'none',
        'length_year': math.floor(DATE_LENGTH/12),
        'length_month': DATE_LENGTH % 12,
        'is_current': True,
        'achievements': ACHIEVEMENTS_API['billy_work'],
        'skills': [],
    }
}
