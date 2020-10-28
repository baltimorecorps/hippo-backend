import json
import pytest

#imports test data
from tests.data.contact_data import CONTACTS_API, EMAILS_API
from tests.data.skill_data import CONTACT_SKILLS
from tests.data.profile_data import PROFILES_API
from tests.data.program_data import PROGRAM_APPS_API


class TestCapabilityRecommended:

    def test_get(self):
        assert 1


class TestContactCapabilitySuggestions:

    def test_post(self):
        assert 1


class TestContactCapabilitySuggestionOne:

    def test_delete(self):
        assert 1


class TestContactCapabilities:

    def test_get(self):
        assert 1
