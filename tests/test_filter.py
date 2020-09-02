import pytest
from pprint import pprint
import json

from models.contact_model import Contact
from resources.Filter import FilterOutputSchema

OUTPUT = {
    'billy': {
        'id': 123,
        'first_name': 'Billy',
        'last_name': 'Daly',
        'email': 'billy@example.com',
        'phone_primary': '555-245-2351',
        'years_exp': '3-5',
        'job_search_status': 'Actively looking',
        'programs': ['Place for Purpose']
    }
}


def test_default_filter(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    payload = {}
    expected = [OUTPUT['billy']]
    output_schema = FilterOutputSchema(many=True)

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
