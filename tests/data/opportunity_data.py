from contact_data import CONTACTS

RESUME_SNAPSHOTS = {
    'snapshot1': {'test': 'snapshot1'}
}

OPPORTUNITIES = {
    'opp1': {
        'id': '123abc',
        'title': "Test Opportunity",
        'short_description': "This is a test opportunity.",
        'gdoc_link': "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        'status': 'submitted',
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
        'status': 'submitted',
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
        'status': 'submitted',
        'org_name': 'Test Org',
        'program_id': 1,
        'is_active': True,
        'program_name': "Place for Purpose"
    },
}

OPPORTUNITY_APPS = {
    'billy1': {
        'id': 'a1',
        'interest_statement': "I'm interested in this test opportunity",
        'status': 'submitted',
        'resume': SNAPSHOTS['snapshot1'],
        'is_active': True,
        'interview_date': None,
        'interview_time': None,
        'interview_completed': False
    },
    'billy2': {
        'id': 'a2',
        'contact': CONTACTS['billy'],
        'opportunity': OPPORTUNITIES['test_opp2'],
        'interest_statement': "I'm also interested in this test opportunity",
        'status': 'draft',
        'resume': None,
        'is_active': True,
        'interview_date': None,
        'interview_time': None,
        'interview_completed': False,
    }
}
