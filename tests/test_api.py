import json

def test_post_one_contact(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "first_name": "Susan",
        "last_name": "Smith",
        # "email_primary": "p@gmail.com",
        "phone_primary": "111-111-1111",
        "gender": "Female",
        "race_all": "White",
        "birthdate": "1973-04-23"
    }
    url = '/api/contacts/'
    with app.test_client() as client:
        # assert there are no contacts
        response = client.get(url)
        assert len(json.loads(response.data)['data']) == 0
        # add contact
        response = client.post(url, data=json.dumps(data), headers=headers)
        assert response.status_code == 201
        # check that contact was added
        response = client.get(url)
        assert response.status_code == 200
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data[0]['id'] is not None
#
def test_post_one_experience(app):
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

def test_put_by_experience_id(app):
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

def test_get_contact_profile(app):
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
