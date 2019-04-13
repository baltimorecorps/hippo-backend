def test_get_all_contacts(app):
    with app.test_client() as client:
        response = client.get('/api/contacts/')

        assert response.status_code == 200


def test_get_all_tags(app):
    with app.test_client() as client:
        response = client.get('/api/tags')

        assert response.status_code == 200
