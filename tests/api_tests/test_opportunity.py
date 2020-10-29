import json
import pytest

#imports test data
from tests.data.contact_data import CONTACTS_API, EMAILS_API
from tests.data.skill_data import CONTACT_SKILLS
from tests.data.profile_data import PROFILES_API
from tests.data.program_data import PROGRAM_APPS_API


class TestOpportunityAll:

    def test_get(self):
        assert 1

    def test_post(self):
        assert 1


class TestOpportunityAllInternal:

    def test_get(self):
        assert 1


class TestOpportunityOneOrg:

    def test_get(self):
        assert 1


class TestOpportunityOne:

    def test_get(self):
        assert 1

    def test_delete(self):
        assert 1

    def test_put(self):
        assert 1


class TestOpportunityDeactivate:

    def test_post(self):
        assert 1


class TestOpportunityActivate:

    def test_post(self):
        assert 1
