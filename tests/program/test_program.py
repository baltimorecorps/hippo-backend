import json
import pytest

#imports test data
from tests.program.program_data import PROGRAMS_API

from tests.utils import get_request_many


class TestProgramAll:

    def test_get(self, app):
        url = '/api/programs'
        expected = PROGRAMS_API.values()

        get_request_many(app, url, expected)
