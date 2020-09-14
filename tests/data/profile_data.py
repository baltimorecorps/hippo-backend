from contact_data import CONTACTS

PROFILES = {
    'billy': {
        **CONTACTS['billy'],
        'profile': {
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
            'programs_completed': {
                'fellowship': False,
                'public_allies': False,
                'mayoral_fellowship': True,
                'kiva': False,
                'elevation_awards': False,
                'civic_innovators': False
            },
            'address_primary': {
                'street1': '123 Main St',
                'street2': 'Apt 3',
                'city': 'Baltimore',
                'state': 'Maryland',
                'zip_code': '21218',
                'country': 'United States',
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
            },
            'roles': {
                'advocacy_public_policy': True,
                'community_engagement_outreach': True,
                'data_analysis': True,
                'fundraising_development': False,
                'program_management': False,
                'marketing_public_relations': False
            }
        }
    },
    'obama': {
        **CONTACTS['obama'],
        'profile': {
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
            'programs_completed': {
                'fellowship': False,
                'public_allies': False,
                'mayoral_fellowship': False,
                'kiva': False,
                'elevation_awards': False,
                'civic_innovators': False,
            },
            'address_primary': {
                'street1': None,
                'street2': None,
                'city': None,
                'state': None,
                'zip_code': None,
                'country': None,
             },
            'race': {
                'american_indian': False,
                'asian': False,
                'black': False,
                'hispanic': False,
                'hawaiian': False,
                'south_asian': False,
                'white': False,
                'not_listed': False,
                'race_other': None,
            },
            'roles': {
                'advocacy_public_policy': False,
                'community_engagement_outreach': False,
                'data_analysis': False,
                'fundraising_development': False,
                'program_management': False,
                'marketing_public_relations': False
            }
        }
    },
}
