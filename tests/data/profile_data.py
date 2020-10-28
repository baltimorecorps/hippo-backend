import copy

from tests.data.contact_data import CONTACTS_API


ADDRESSES = {
    'billy': {
        'street1': '123 Main St',
        'street2': 'Apt 3',
        'city': 'Baltimore',
        'state': 'Maryland',
        'zip_code': '21218',
        'country': 'United States',
        'is_primary': True
    },
    'obama': {
        'street1': None,
        'street2': None,
        'city': None,
        'state': None,
        'zip_code': None,
        'country': None,
        'is_primary': True
    }
}

PROGRAMS_COMPLETED = {
    'billy': {
        'fellowship': False,
        'public_allies': False,
        'mayoral_fellowship': True,
        'kiva': False,
        'elevation_awards': False,
        'civic_innovators': False
    },
    'obama': {
        'fellowship': False,
        'public_allies': False,
        'mayoral_fellowship': False,
        'kiva': False,
        'elevation_awards': False,
        'civic_innovators': False,
    }
}

RACE = {
    'billy': {
        'american_indian': False,
        'asian': False,
        'black': False,
        'hispanic': False,
        'hawaiian': False,
        'south_asian': False,
        'white': True,
        'not_listed': False,
        'race_other': None,
    },
    'obama': {
        'american_indian': False,
        'asian': False,
        'black': False,
        'hispanic': False,
        'hawaiian': False,
        'south_asian': False,
        'white': False,
        'not_listed': False,
        'race_other': None,
    }
}

ROLES = {
    'billy': {
        'advocacy_public_policy': True,
        'community_engagement_outreach': True,
        'data_analysis': True,
        'fundraising_development': False,
        'program_management': False,
        'marketing_public_relations': False
    },
    'obama': {
        'advocacy_public_policy': False,
        'community_engagement_outreach': False,
        'data_analysis': False,
        'fundraising_development': False,
        'program_management': False,
        'marketing_public_relations': False
    }
}

PROFILES_DATABASE = {
    'billy': {
        'id': 123,
        'gender': 'Male',
        'gender_other': None,
        'pronoun': 'He/Him/His',
        'pronoun_other': None,
        'years_exp': '3-5',
        'job_search_status': 'Actively looking',
        'current_job_status': 'Employed',
        'current_edu_status': 'Full-time Student',
        'previous_bcorps_program': 'Yes',
        'value_question1': 'Test response',
        'value_question2': 'Test response',
        'needs_help_programs': True,
        'hear_about_us': 'Facebook',
        'hear_about_us_other': 'Other',
    },
    'obama': {
        'id': 1,
        'gender': None,
        'gender_other': None,
        'pronoun': None,
        'pronoun_other': None,
        'years_exp': None,
        'job_search_status': None,
        'current_job_status': None,
        'current_edu_status': None,
        'previous_bcorps_program': None,
        'value_question1': None,
        'value_question2': None,
        'hear_about_us': None,
        'hear_about_us_other': None,
        'needs_help_programs': None,
    }
}

PROFILES_API = {
    'billy': {
        **CONTACTS_API['billy'],
        'profile': {
            **PROFILES_DATABASE['billy'],
            'programs_completed': PROGRAMS_COMPLETED['billy'],
            'address_primary': ADDRESSES['billy'],
            'race': RACE['billy'],
            'roles': ROLES['billy'],
        }
    },
    'obama': {
        **CONTACTS_API['obama'],
        'profile': {
            **PROFILES_DATABASE['obama'],
            'programs_completed': PROGRAMS_COMPLETED['obama'],
            'address_primary': ADDRESSES['obama'],
            'race': RACE['obama'],
            'roles': ROLES['obama'],
        }
    }
}

# creates billy_update
billy_update = copy.deepcopy(PROFILES_API['billy'])
billy_update['email'] = "billy_new@email.com"
billy_update['profile']['address_primary']['street1'] = '124 Main St'
billy_update['profile']['roles']['data_analysis'] = False
billy_update['profile']['race']['hispanic'] = True
billy_update['profile']['race']['not_listed'] = True
billy_update['profile']['race']['race_other'] = 'Test Text'
PROFILES_API['billy_update'] = billy_update

# creates billy_null
billy_null = copy.deepcopy(PROFILES_API['billy'])
del billy_null['profile']['programs_completed']
PROFILES_API['billy_null'] = billy_null
