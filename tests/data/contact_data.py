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
