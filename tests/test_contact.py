import json
from flask import url_for

def test_add_contact(app):
    # print(app)
    with app.test_client() as client:
        response =client.get(url_for('contacts'), follow_redirects=True)
        # response = client.post('/contacts',
        #                         data=json.dumps(dict(
        #                         first_name= "abc",
        #                         last_name= "xyz",
        #                         email_primary= "p@gmail.com",
        #                         phone_primary="111-111-1111",
        #                         gender= "Female",
        #                         race_all= "Asian",
        #                         birthdate= "2012-04-23"
        #                         )),
        #                         content_type='application/json'
        #                        )
        #data = json.loads(response.data.decode())

        assert response.json =={
                                    "status": "success",
                                    "data": []
                                }