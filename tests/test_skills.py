import pytest

from resources.skill_utils import normalize_skill_name, get_skill_id, Autocomplete

@pytest.mark.parametrize(
    "arg,expected",
    [('Python', 'python')
    ,('C++', 'c++')
    ,('a/v', 'a v')
    ,('anti-racism', 'anti racism')
    ,('mod_perl', 'mod perl')
    ,('art   	history', 'art history')
    ,('ASP.NET', 'asp.net')
    ,('(ACO)', 'aco')
    ,(' whitespace   ', 'whitespace')
    ,('unicodeßÄ①Ⅰ', 'unicodessä1i')
    ]
)
def test_normalize(arg, expected):
    assert normalize_skill_name(arg) == expected

@pytest.mark.parametrize(
    "arg,expected",
    [('python', '4R9tqGuK2672PavRTJrN/A==')
    ,('C++', 'sEVDZsMOqdfQ+vwoIAEk5A==')
    ,(' c++  ', 'sEVDZsMOqdfQ+vwoIAEk5A==')
    ]
)
def test_get_id(arg, expected):
    assert get_skill_id(arg) == expected


@pytest.fixture
def autocomplete():
    return Autocomplete(['Aaa', 'Aab', 'Abc'])

class TestAutocomplete:
    def test_match(self, autocomplete):
        matches = autocomplete.match('Aa')
        assert len(matches) == 2
        assert matches[0] == 'Aaa'
        assert matches[1] == 'Aab'

    def test_match_single(self, autocomplete):
        matches = autocomplete.match('Abc')
        assert len(matches) == 1
        assert matches[0] == 'Abc'

    def test_match_empty(self, autocomplete):
        matches = autocomplete.match('')
        assert len(matches) == 3
        assert matches[0] == 'Aaa'
        assert matches[1] == 'Aab'
        assert matches[2] == 'Abc'

    def test_match_case(self, autocomplete):
        matches = autocomplete.match('aA')
        assert len(matches) == 2
        assert matches[0] == 'Aaa'
        assert matches[1] == 'Aab'


