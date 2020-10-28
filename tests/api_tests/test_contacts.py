import json
import pytest

#imports test data
from tests.data.contact_data import CONTACTS_API, EMAILS_API
from tests.data.skill_data import CONTACT_SKILLS
from tests.data.profile_data import PROFILES_API
from tests.data.program_data import PROGRAM_APPS_API

CONTACTS = {
    'billy': {
        **CONTACTS_API['billy'],
        'email_primary': EMAILS_API['billy'],
        'skills': CONTACT_SKILLS['billy'],
        'program_apps': PROGRAM_APPS_API['billy']['program_apps'],
        'profile': PROFILES_API['billy']['profile']
    },

    'obama': {
        **CONTACTS_API['obama'],
        'email_primary': EMAILS_API['obama'],
        'skills': CONTACT_SKILLS['obama'],
        'program_apps': [],
        'profile': None
    }
}

class TestContactAll:

    def test_post(self):
        assert 1


class TestContactShort:

    def test_get(self):
        assert 1


class TestContactAccount:

    def test_get(self):
        assert 1

class TestContactOne:

    def test_get(self):
        assert 1

    def test_put(self):
        assert 1

    def test_delete(self):
        assert 1

class TestContactFull:

    def test_get(self):
        assert 1

class TestContactApproveMany:

    def test_post(self):
        assert 1
