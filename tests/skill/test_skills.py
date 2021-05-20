import pytest

from app.resources.skill_utils import normalize_skill_name, get_skill_id, Autocomplete

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
    [('python', '4R9tqGuK2672PavRTJrN_A==')
    ,('C++', 'sEVDZsMOqdfQ-vwoIAEk5A==')
    ,(' c++  ', 'sEVDZsMOqdfQ-vwoIAEk5A==')
    ]
)
def test_get_id(arg, expected):
    assert get_skill_id(arg) == expected

MATCH_STRINGS = ['Aaa', 'Aab', 'Abc', 'Bbb Bbb', 'C++', 'Caa']

@pytest.fixture
def autocomplete():
    return Autocomplete(MATCH_STRINGS)

def get_matches(match_result):
    return match_result['matches']

class TestAutocomplete:
    def test_match(self, autocomplete):
        matches = get_matches(autocomplete.match('Aa'))
        assert len(matches) == 2
        assert matches[0] == 'Aaa'
        assert matches[1] == 'Aab'

    def test_match_single(self, autocomplete):
        matches = get_matches(autocomplete.match('Abc'))
        assert len(matches) == 1
        assert matches[0] == 'Abc'

    def test_match_empty(self, autocomplete):
        matches = get_matches(autocomplete.match(''))
        assert len(matches) == len(MATCH_STRINGS)
        assert matches == MATCH_STRINGS

    def test_match_case(self, autocomplete):
        matches = get_matches(autocomplete.match('aA'))
        assert len(matches) == 2
        assert matches[0] == 'Aaa'
        assert matches[1] == 'Aab'

    def test_match_spaces(self, autocomplete):
        matches = get_matches(autocomplete.match('Bbb'))
        assert len(matches) == 1
        assert matches[0] == 'Bbb Bbb'

    def test_match_punctuation(self, autocomplete):
        result = autocomplete.match('C++')
        matches = get_matches(result)
        assert len(matches) == 1
        assert matches[0] == 'C++'
        assert result['got_exact']


    def test_exact(self, autocomplete):
        result = autocomplete.match('Aaa')
        assert result['got_exact'] 
        assert get_matches(result)[0] == 'Aaa', "Exact result should be first"

        result = autocomplete.match('Bbb')
        assert not result['got_exact'] 

    def test_no_results(self, autocomplete):
        result = autocomplete.match('ZZZ')
        assert not result['got_exact'] 
        assert len(get_matches(result)) == 0

