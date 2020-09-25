# This is what is set in the database in populate_db.py
CONTACTS_DATABASE = {
    'billy': {
        'id': 123,
        'first_name': "Billy",
        'last_name': "Daly",
        'email': "billy@example.com",
        'phone_primary': "555-245-2351",
        'account_id': 'test-valid|0123456789abcdefabcdefff',
    },
    'obama': {
        'id': 124,
        'first_name': "Barack",
        'last_name': "Obama",
        'email': "obama@whitehouse.gov",
        'phone_primary': "555-444-4444",
        'account_id': 'test-valid|alsghldwgsg120393020293',
    }
}

EMAILS_DATABASE = {
    'billy': {
        'id': 45,
        'is_primary': True,
        'email': "billy@example.com",
    },
    'obama': {
        'id': 90,
        'is_primary': True,
        'email': "obama@whitehouse.gov",
    }
}


# This is what is returned in the API
CONTACTS_API = {
    'billy': {**CONTACTS_DATABASE['billy'], 'status': 'approved'},
    'obama': {**CONTACTS_DATABASE['obama'], 'status': 'created'}
}

EMAILS_API = {
    'billy': {**EMAILS_DATABASE, 'type': 'Personal'},
    'obama': {**EMAILS_DATABASE, 'type': 'Work'}

}

INSTRUCTIONS_API = {
    'billy': {
        **CONTACTS_API['billy'],
        'instructions': {
            'about_me': {
                'is_complete': True,
                'components': {
                    'candidate_information': True,
                    'value_alignment': True,
                    'programs': True,
                    'interests': True,
                },
            },
            'profile': {
                'is_complete': True,
                'components': {
                    'tag_skills': True,
                    'add_experience': {
                        'is_complete': True,
                        'components': {
                            'add_achievements': True,
                            'tag_skills': True,
                        }
                    },
                    'add_education': True,
                    'add_portfolio': False,
                },
            },
            'submit': {'is_complete': True}
        }
    },
    'obama': {
        **CONTACTS_API['obama'],
        'instructions': {
            'about_me': {
                'is_complete': False,
                'components': {
                    'candidate_information': False,
                    'value_alignment': False,
                    'programs': False,
                    'interests': False,
                },
            },
            'profile': {
                'is_complete': False,
                'components': {
                    'tag_skills': False,
                    'add_experience': {
                        'is_complete': False,
                        'components': {
                            'add_achievements': False,
                            'tag_skills': False,
                        }
                    },
                    'add_education': False,
                    'add_portfolio': True,
                },
            },
            'submit': {'is_complete': False}
        }
    }
}
