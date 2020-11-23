import json
from pprint import pprint
import pytest

def skill_name(skill):
    return skill.name

def post_request(app, url, data):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    with app.test_client() as client:
        response = client.post(url, data=json.dumps(data),
                               headers=headers)
        print('RESPONSE')
        pprint(response.json)
        assert response.status_code == 201

        data = json.loads(response.data)['data']
        print('DATA')
        pprint(data)
        assert len(data) > 0
        assert data['id'] is not None
        id = data['id']
        return id, data


def put_request(app, url, update, query, test):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        assert query() is not None, "Item to update should exist"
        assert not test(query())
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200
        assert test(query())

def get_request_one(app, url, expected):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        response = client.get(url, headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']
        print('DATA')
        pprint(data)
        print('EXPECTED')
        pprint(expected)
        assert len(data) > 0
        assert data == expected

def get_request_many(app, url, expected):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        response = client.get(url, headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']

        # Test that the data and expected contain the same items, but not
        # necessarily in the same order
        print('EXPECTED')
        pprint(list(expected))
        print('DATA')
        pprint(data)
        assert len(data) == len(expected)
        for item in data:
            pprint(item)
            assert item in expected

def delete_request(app, delete_url, query):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        assert query() is not None, "Item to delete should exist"

        response = client.delete(delete_url, headers=headers)
        assert response.status_code == 200
        assert query() is None, "Deleted item should not exist"
