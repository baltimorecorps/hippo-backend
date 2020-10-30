import json
import pytest

#imports test data
from tests.data.contact_data import CONTACTS_API, EMAILS_API
from tests.data.skill_data import CONTACT_SKILLS
from tests.data.profile_data import PROFILES_API
from tests.data.program_data import PROGRAM_APPS_API


class TestOpportunityAppAll:

    def test_get(self):
        assert 1


class TestOpportunityAppOne:

    def test_get(self):
        assert 1

    def test_post(self):
        assert 1

    def test_put(self):
        assert 1

class TestOpportunityAppReopen:

    def test_post(self):
        assert 1


class TestOpportunityAppSubmit:

    def test_post(self):
        assert 1


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
