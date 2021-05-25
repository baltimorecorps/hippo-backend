import re
import unicodedata
import base64
from hashlib import blake2b

from app.resources.skill_list import SKILL_LIST
from app.schemas import (
    CapabilitySchema,
    SkillSchema,
    SkillRecommendationSchema,
)
from app.models import (
    Skill,
    ContactSkill,
    Capability,
    CapabilitySkillSuggestion,
    Skill,
)

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
    return base64.urlsafe_b64encode(blake2b(skill_bytes, digest_size=16).digest()).decode('utf8')

def get_contact_skill(contact_id, skill_name):
    return (ContactSkill.query
                        .filter_by(contact_id=contact_id,
                                   skill_id=get_skill_id(skill_name))
                        .first())

def make_skill(name):
    return Skill(
        id=get_skill_id(name),
        name=name,
    )

def get_or_make_skill(name):
    id_ = get_skill_id(name)
    skill = Skill.query.get(id_)
    if not skill:
        skill = make_skill(name)
    return skill

skill_schema = SkillSchema()
capability_names_schema = CapabilitySchema(only=('id','name'), many=True)
def dump_skill_with_capabilities(skill, contact_id):
    result = skill_schema.dump(skill)
    result['capabilities'] = capability_names_schema.dump(skill.capabilities)
    result['suggested_capabilities'] = capability_names_schema.dump(
        Capability.query
        .join(CapabilitySkillSuggestion,
              Capability.id == CapabilitySkillSuggestion.capability_id)
        .filter(CapabilitySkillSuggestion.skill_id==skill.id)
        .filter(CapabilitySkillSuggestion.contact_id==contact_id)
        .all())
    return result


def _sort_key(match):
    # Put all exact matches first
    return (not match['exact'], match['item'])

class Autocomplete(object):
    def __init__(self, items):
        self.lookup = {}
        for item in items:
            self.lookup[normalize_skill_name(item)] = item

    def get_scores(self, query):
        prefix = normalize_skill_name(query)
        return [self._make_score(query, prefix, value)
            for (key, value) in self.lookup.items()
            if key.startswith(prefix)]

    def sort_scores(self, scored_items):
        return sorted(scored_items, key=_sort_key)

    def match(self, query):
        results = self.sort_scores(self.get_scores(query))
        got_exact = len(results) > 0 and results[0]['exact']
        # Exact matches should aways come first
        return {
            'matches': [x['item'] for x in results],
            'got_exact': got_exact
        }

    def _make_score(self, query, prefix, value):
        exact_match = (prefix == normalize_skill_name(value))
        return {
            'item': value,
            'exact': exact_match,
        }

_instance = None
def _autocomplete():
    global _instance
    if _instance is None:
        _instance = Autocomplete(SKILL_LIST)
    return _instance

def complete_skill(skill):
    return _autocomplete().match(skill)
