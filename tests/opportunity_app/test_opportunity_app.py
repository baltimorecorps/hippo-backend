import json
import datetime as dt
from pprint import pprint
import pytest
import math
import copy

from models.opportunity_app_model import OpportunityApp, ApplicationStage

#imports test data
from tests.opportunity.opportunity_data import OPPS_API, OPP_APPS_API, OPPS_INTERNAL_API

# imports testing utils
from tests.utils import (
    post_request,
    get_request_one,
    get_request_many,
    put_request,
    delete_request,
    skill_name
)

class TestOpportunityAppAll:

    def test_get(self):
        assert 1


class TestOpportunityAppOne:

    def test_get(self):
        assert 1

    def test_post(self):
        assert 1

    @pytest.mark.parametrize(
        "url,update,query,test",
        [('/api/contacts/123/app/123abc',
        {'interest_statement': "New interest statement", 'resume': None},
        lambda: OpportunityApp.query.get('a1'),
        lambda r: r.interest_statement == 'New interest statement',
        )
        ,('/api/contacts/123/app/123abc',
        {'resume': {'test': 'snapshotnew'}},
        lambda: OpportunityApp.query.get('a1'),
        lambda r: r.resume.resume == '{"test":"snapshotnew"}',
        )
        ,('/api/contacts/123/app/222abc',
        {'resume': {'test': 'snapshotnew'}},
        lambda: OpportunityApp.query.get('a2'),
        lambda r: r.resume and r.resume.resume == '{"test":"snapshotnew"}',
        )
        ,('/api/contacts/123/app/123abc',
        OPP_APPS_API['billy_update'],
        lambda: OpportunityApp.query.get('a1'),
        lambda r: r.interest_statement == 'dfdddsdfff',
        )
    ])

    def test_put(self, app, url, update, query, test):
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

class TestOpportunityAppReopen:

    def test_post(self):
        assert 1


class TestOpportunityAppSubmit:
    @pytest.mark.parametrize(
        "url,data,query",
        [pytest.param('/api/contacts/124/app/333abc/',
      {},
      lambda id: (OpportunityApp.query
                  .filter_by(contact_id=124, opportunity_id='123abc').first()),
      )])

    def test_post(self,app, url, data, query):
        mimetype = 'application/json'
        headers = {
            'Content-Type': mimetype,
            'Accept': mimetype
        }

        id_, _ = post_request(app, url, data)
        assert query(id_) is not None

    def test_post_opportunity_app_status(self,app):
        id_, _ = post_request(app, '/api/contacts/124/app/333abc/', {})
        assert OpportunityApp.query.get(id_).stage == ApplicationStage.draft.value


class TestOpportunityAppRecommend:

    def test_post(self):
        assert 1


class TestOpportunityAppReject:

    def test_post(self):
        assert 1


class TestOpportunityAppInterview:

    def test_post(self):
        assert 1


class TestOpportunityAppConsider:

    def test_post(self):
        assert 1
