import json
from flask import url_for

def test_add_contact(app):
    # print(app)
    with app.test_client() as client:
        response =client.get('/contacts/')

        assert response.status_code == 200