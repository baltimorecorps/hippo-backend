import json
import pytest

from tests.profile.profile_data import PROFILES_API

# imports testing utils
from tests.utils import (
    post_request,
    get_request_one,
    get_request_many,
    put_request,
    delete_request,
    skill_name
)


class TestProfileOne:

    def test_get(self, app):
        url = '/api/contacts/123/about-me'
        expected = PROFILES_API['billy']

        get_request_one(app, url, expected)


    def test_post(self):
        assert 1

    def test_put(self):
        assert 1


class TestContactInstructions:

    def test_get(self):
        assert 1


class TestProfileSubmit:

    def test_post(self):
        assert 1
