import re
import unicodedata
import base64
from hashlib import blake2b

from flask import request as reqobj
from flask_restful import Resource, request
from models.skill_model import SkillItem, SkillItemSchema
from marshmallow import ValidationError

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


class Skills(Resource):
    pass

