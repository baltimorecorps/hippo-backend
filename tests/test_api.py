import json
import pytest

"""
* GET api/contacts/
POST api/contacts/
GET api/contacts/<int:contact_id>/
GET api/contacts/<int:contact_id>/
GET api/contacts/<contact_id>/experiences/
POST api/contacts/<contact_id>/experiences/
GET api/experiences/<int:exp_id>/
PUT api/experiences/<int:exp_id>/
DELETE api/experiences/<int:exp_id>/
GET api/tags/
POST api/tags/
GET api/tags/<tag_id>/
GET api/contacts/<contact_id>/tags/
POST api/contacts/<contact_id>/tags/
PUT api/contacts/<contact_id>/tags/<tag_item_id>/
GET api/contacts/<int:contact_id>/achievements/
GET api/contact/<contact_id>/resumes/
POST api/contacts/<contact_id>/resumes/
GET api/resumes/<int:resume_id>/
PUT api/resumes/<resume_id>/
DELETE api/resumes/<resume_id>/
GET api/resumes/<resume_id>/sections/
POST api/resumes/<resume_id>/sections/<section_id>/
GET api/resumes/<resume_id>/sections/<section_id>/
PUT api/resumes/<resume_id>/sections/<section_id>/
DELETE api/resumes/<int:section_id>/sections/<section_id>/
"""

CONTACTS = {
    'billy': {
        'id': 123,
        'first_name': "Billy",
        'last_name': "Daly",
        'email_primary': {
            'id': 45,
            'is_primary': True,
            'email': "billy@example.com",
            'type': "Personal",
        },
        'emails': [{
            'id': 45,
            'is_primary': True,
            'email': "billy@example.com",
            'type': "Personal",
        }],
        'gender': 'Male',
        'birthdate': '1991-01-02',
        'phone_primary': "555-245-2351",
        'race_all': "White",
    },

    'obama': {
        'id': 124,
        'first_name': "Barack",
        'last_name': "Obama",
        'email_primary': {
            'id': 90,
            'is_primary': True,
            'email': "obama@whitehouse.gov",
            'type': "Work",
        },
        'emails': [{
            'id': 90,
            'is_primary': True,
            'email': "obama@whitehouse.gov",
            'type': "Work",
        }],
        'gender': 'Male',
        'birthdate': '1961-08-04',
        'phone_primary': "555-444-4444",
        'race_all': "Black",
    }
}

TAGS = {
    'python': {
        'id': 123,
        'name': 'Python',
        'type': 'Skill',
        'status': 'Active',
    },
    'webdev': {
        'id': 124,
        'name': 'Web Development',
        'type': 'Function',
        'status': 'Active',
    },
    'health': {
        'id': 125,
        'name': 'Public Health',
        'type': 'Topic',
        'status': 'Active',
    }
}




@pytest.mark.parametrize(
    "url,expected",
    [('/api/contacts/123/', CONTACTS['billy'])
    ,('/api/contacts/124/', CONTACTS['obama'])
    ]
)
def test_get(app, url, expected):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        response = client.get(url, headers=headers)
        print(response)
        assert response.status_code == 200
        data = json.loads(response.data)['data']
        assert len(data) > 0
        print(json.loads(response.data))
        assert data == expected


def est_post_one_contact(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "first_name": "Susan",
        "last_name": "Smith",
        "email_primary": {
            "email": "p@gmail.com",
            "is_primary": True, 
        },
        "phone_primary": "111-111-1111",
        "gender": "Female",
        "race_all": "White",
        "birthdate": "1973-04-23"
    }
    url = '/api/contacts/'
    with app.test_client() as client:
        response = client.post(url, data=json.dumps(data), headers=headers)
        assert response.status_code == 201
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data['id'] is not None

        response = client.get(url + str(data['id']) + '/')
        assert response.status_code == 200
        print(json.loads(response.data))
        assert true == false

#
def est_post_one_experience(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    exp_data = {
        "description": "Tutored after-school",
        "host": "BPL",
        "title": "Volunteer",
        "date_start": "2000-01-01",
        "date_end": "2010-01-01",
        "type": "Service"
    }
    contact_data = {
        "first_name": "Susan",
        "last_name": "Smith",
        # "email_primary": "p@gmail.com",
        "phone_primary": "111-111-1111",
        "gender": "Female",
        "race_all": "White",
        "birthdate": "1973-04-23"
    }
    contact_url = '/api/contacts/'
    with app.test_client() as client:
        # add contact
        response = client.post(contact_url, data=json.dumps(contact_data), headers=headers)
        assert response.status_code == 201
        contact_id = json.loads(response.data)['data']['id']
        exp_url = contact_url + str(contact_id) + '/experiences/'
        response = client.get(exp_url)
        # assert experience list is empty
        assert len(json.loads(response.data)['data']) == 0
        # add experience to that contact using contact_id
        response = client.post(exp_url, data=json.dumps(exp_data), headers=headers)
        assert response.status_code == 201
        response = client.get(exp_url)
        # assert experience list is not empty
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data[0]['id'] is not None

def est_put_by_experience_id(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    exp_data = {
        "description": "Tutored after-school",
        "host": "BPL",
        "title": "Volunteer",
        "date_start": "2000-01-01",
        "date_end": "2010-01-01",
        "type": "Service"
    }
    contact_data = {
        "first_name": "Susan",
        "last_name": "Smith",
        # "email_primary": "p@gmail.com",
        "phone_primary": "111-111-1111",
        "gender": "Female",
        "race_all": "White",
        "birthdate": "1973-04-23"
    }
    update_data = {
        "type": "Work"
    }
    contact_url = '/api/contacts/'
    with app.test_client() as client:
        #add contact to db
        response = client.post(contact_url, data=json.dumps(contact_data), headers=headers)
        assert response.status_code == 201
        contact_id = json.loads(response.data)['data']['id']
        exp_url = contact_url + str(contact_id) + '/experiences/'
        #add experience to that contact using contact_id
        response = client.post(exp_url, data=json.dumps(exp_data), headers=headers)
        assert response.status_code == 201
        data = json.loads(response.data)['data']
        assert data['type'] == "Service"
        exp_id = data['id']
        upd_url = exp_url + str(exp_id)
        #update that experience using exp_id
        response = client.put(upd_url, data=json.dumps(update_data), headers=headers)
        assert response.status_code == 201
        #check that it was updated properly
        response = client.get(upd_url)
        assert response.status_code == 200
        assert json.loads(response.data)['data']['type'] == "Work"

def est_get_contact_profile(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "first_name": "Amy",
        "last_name": "Smith",
        # "email_primary": "amy@yahoo.com",
        "phone_primary": "401-234-1124",
        "gender": "Female",
        "race_all": "White",
        "birthdate": "1983-02-09"
    }
    url = '/api/contacts/'
    with app.test_client() as client:
        # add contact
        response = client.post(url, data=json.dumps(data), headers=headers)
        assert response.status_code == 201
        data = json.loads(response.data)['data']
        id = data['id']
        profile_url = url + str(id) + "/profile"
        # check that a profile exists
        response = client.get(profile_url)
        assert response.status_code == 200
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data['service_experience'] is not None


