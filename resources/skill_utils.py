import re
import unicodedata
import base64
from hashlib import blake2b

from models.skill_model import SkillItem

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


if __name__ == '__main__':
    import sys
    print(get_skill_id(sys.argv[1]))
