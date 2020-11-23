import json
import pytest
import unittest
from pprint import pprint

from models.base_model import db
from models.opportunity_model import Opportunity
from models.opportunity_app_model import OpportunityApp, ApplicationStage
#imports test data


OPP_POST_PAYLOAD = {
      'opportunity': {
        "title": "Test Opportunity",
        "short_description": "We are looking for a tester to test our application by taking this test opportunity. Testers of all experience welcome",
        "gdoc_id": "TESTABC11==",
        "cycle_id": 1,
        "org_name": 'Test Org',
        "gdoc_link": "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        "is_active": True,
        'program_name': "Place for Purpose"
    },
    'mayoral_opportunity': {
        "title": "Mayoral Test 1",
        "short_description": "We are looking for a tester to test our application by taking this test opportunity. Testers of all experience welcome",
        "gdoc_id": "TESTABC11==",
        "org_name": 'Test Org',
        "gdoc_link": "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        "is_active": True,
        'program_name': "Mayoral Fellowship"
    },
    'blank_opportunity': {
        "title": "Blank Test 1",
        "short_description": "We are looking for a tester to test our application by taking this test opportunity. Testers of all experience welcome",
        "gdoc_id": "TESTABC11==",
        "org_name": 'Test Org',
        "gdoc_link": "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        "is_active": True,
        'program_name': None,
    }
   
}

def post_request(app, url, data):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    with app.test_client() as client:
        response = client.post(url, data=json.dumps(data),
                               headers=headers)
        pprint(response.json)
        assert response.status_code == 201
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data['id'] is not None
        id = data['id']
        return id, data

@pytest.mark.parametrize("url,data,query",
    [(('/api/opportunity/',
        OPP_POST_PAYLOAD['opportunity'],
        lambda id: Opportunity.query.filter_by(title="Test Opportunity").first()
    ))])

def test_post(app, url, data, query):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    id_, _ = post_request(app, url, data)
    assert query(id_) is not None

@pytest.mark.parametrize(
        "data,program_id",
        [(OPP_POST_PAYLOAD['opportunity'], 1),
        (OPP_POST_PAYLOAD['mayoral_opportunity'], 2),
        (OPP_POST_PAYLOAD['blank_opportunity'], 1)]
    )
def test_post_opp_program(app, data, program_id):
    id_, data = post_request(app, '/api/opportunity/', data)
    opp = Opportunity.query.filter_by(title=data['title']).first()
    assert opp is not None
    assert opp.program_id == program_id

class TestOpportunityAll(unittest.TestCase):

    def test_get(app):
        assert 1

                
    # @pytest.mark.parametrize(
    #     "data,program_id",
    #     [(OPP_POST_PAYLOAD['opportunity'], 1),
    #     (OPP_POST_PAYLOAD['mayoral_opportunity'], 2),
    #     (OPP_POST_PAYLOAD['blank_opportunity'], 1)]
    # )
    # def test_post_opp_program(app, data, program_id):
    #     id_, data = post_request(app, '/api/opportunity/', data)
    #     opp = Opportunity.query.filter_by(title=data['title']).first()
    #     assert opp is not None
    #     assert opp.program_id == program_id

# class TestOpportunityAllInternal:

#     def test_get(self):
#         assert 1


# class TestOpportunityOneOrg:

#     def test_get(self):
#         assert 1


# class TestOpportunityOne:

#     def test_get(self):
#         assert 1

#     def test_delete(self):
#         assert 1

#     def test_put(self):
#         assert 1


# class TestOpportunityDeactivate:

#     def test_post(self):
#         assert 1


# class TestOpportunityActivate:

#     def test_post(self):
#         assert 1