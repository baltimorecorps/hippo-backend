import re
import unicodedata
import base64
from hashlib import blake2b

from models.skill_model import SkillItem
from .skill_list import SKILL_LIST

TO_WHITESPACE = str.maketrans('-/_()', '     ')

def normalize_skill_name(skill):
    # Make sure weird unicode stuff doesn't break our normalization
    # See https://unicode.org/reports/tr15/
    skill = unicodedata.normalize('NFKC', skill)
    skill = skill.casefold().translate(TO_WHITESPACE).strip()
    skill = re.sub(r'\s+',' ', skill) # replace whitespace
    return skill

def get_skill_id(skill):
    skill_bytes = normalize_skill_name(skill).encode('utf8');
    return base64.b64encode(blake2b(skill_bytes, digest_size=16).digest()).decode('utf8')

def make_skill(name, contact_id):
    return SkillItem(
        id=get_skill_id(name),
        name=name,
        contact_id=contact_id
    )

class Autocomplete(object):
    def __init__(self, items):
        self.lookup = {}
        for item in items:
            self.lookup[normalize_skill_name(item)] = item 

    def get_scores(self, query):
        prefix = normalize_skill_name(query)
        return [self._make_score(value)
            for (key, value) in self.lookup.items()
            if key.startswith(prefix)]

    def sort_scores(self, scored_items):
        return sorted(scored_items, key=lambda x: x['item'])

    def match(self, query):
        return [
            x['item'] for x in self.sort_scores(self.get_scores(query))
        ]

    def _make_score(self, value):
        return {
            'item': value,
        }

_instance = None
def _autocomplete():
    global _instance
    if _instance is None:
        _instance = Autocomplete(SKILL_LIST)
    return _instance

def complete_skill(skill):
    return _autocomplete().match(skill)

if __name__ == '__main__':
    import sys
    print(get_skill_id(sys.argv[1]))
