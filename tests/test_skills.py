import pytest

from resources.skill_utils import normalize_skill_name, get_skill_id

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


