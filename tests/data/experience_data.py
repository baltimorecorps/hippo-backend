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
    'bily_work3': {
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
        'description': 'Test description',
        'host': 'Columbia University',
        'title': 'Political Science',
        'degree': None,
        'degree_other': None,
        'link': 'www.google.com',
        'link_name': 'Google',
        'is_current': False,
        'start_month': 'September',
        'start_year': 1979,
        'end_month': 'May',
        'end_year': 1983,
        'type': 'Accomplishment',
        'contact_id': 124,
        'location': 'New York, NY, USA',
    },
    'billy_edu': {
        'id': 512,
        'description': None,
        'host': 'Goucher College',
        'title': 'Economics',
        'degree': 'Undergraduate',
        'degree_other': 'Study Abroad',
        'link': None,
        'link_name': None,
        'is_current': False,
        'start_month': 'September',
        'start_year': 2012,
        'end_month': 'May',
        'end_year': 2016,
        'type': 'Education',
        'contact_id': 123,
        'location': 'Towson, MD, USA',
    },
    'billy_work' : {
        'id': 513,
        'description': 'Test description here',
        'host': 'Baltimore Corps',
        'title': 'Systems Design Manager',
        'degree': None,
        'degree_other': None,
        'link': None,
        'link_name': None,
        'is_current': True,
        'start_month': 'January',
        'start_year': 2000,
        'end_month': 'none',
        'end_year': 0,
        'type': 'Work',
        'contact_id': 123,
        'location': 'Baltimore, MD, USA',
    },
}

ACHIEVEMENTS_API = {
    'billy_work': [
        {**ACHIEVEMENTS_DATABASE['billy_work1'],
         'skills': []},
        {**ACHIEVEMENTS_DATABASE['billy_work1'],
         'skills': []},
    ]
    },
    'billy_edu1': [
        {**ACHIEVEMENTS_DATABASE['billy_edu'],
         'skills': []}
    ]
}

EXPERIENCES_API ={
    'obama_portfolio': {
        **EXPERIENCES_DATABASE['obama_portfolio'],
        'length_year': 3,
        'length_month': 8,
        'achievements': [],
        'skills': [],
    },
    'billy_edu': {
        **EXPERIENCES_DATABASE['billy_edu'],
        'length_year': 3,
        'length_month': 8,
        'achievements': ACHIEVEMENTS_API['billy_edu'],
        'skills': [],
    },
    'billy_work': {
        **EXPERIENCES_DATABASE['billy_work'],
        'length_year': math.floor(DATE_LENGTH/12),
        'length_month': DATE_LENGTH % 12,
        'acheivements': ACHIEVEMENTS_API['billy_work']
    }
}
