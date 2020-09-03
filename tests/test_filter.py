import pytest
from pprint import pprint
import json

from models.contact_model import Contact

OUTPUT = {
    'with_programs': {
        'id': 123,
        'first_name': 'Billy',
        'last_name': 'Daly',
        'email': 'billy@example.com',
        'status': 'approved',
        'phone_primary': '555-245-2351',
        'years_exp': '3-5',
        'job_search_status': 'Actively looking',
        'programs': ['Place for Purpose']
    },
    'without_programs': {
        'id': 123,
        'first_name': 'Billy',
        'last_name': 'Daly',
        'email': 'billy@example.com',
        'status': 'approved',
        'phone_primary': '555-245-2351',
        'years_exp': '3-5',
        'job_search_status': 'Actively looking'
    }
}


@pytest.mark.parametrize(
    "query,expected",
    [({}, OUTPUT['with_programs']),
     ({'status': ['submitted']}, OUTPUT['without_programs'])]
)
def test_default_filter(app, query, expected):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    payload = query
    expected = [expected]

    with app.test_client() as client:
        response = client.post('/api/contacts/filter',
                               data=json.dumps(payload),
                               headers=headers)

        assert response.status_code == 201

        data = response.json['data']
        print('DATA:')
        pprint(data)
        print('EXPECTED:')
        pprint(expected)
        assert data == expected
