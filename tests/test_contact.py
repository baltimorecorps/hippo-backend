import json

def test_add_contact(app):
    # print(app)
    with app.test_client() as client:
        response =client.get('/contacts')
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
        # print(response)
        # data = json.loads(response.data.decode())
        # print(data)
        assert response.status_code == 201
