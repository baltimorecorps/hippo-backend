from pprint import pprint
import json

import pytest

from models.contact_model import Contact
from models.experience_model import Experience, Month
from models.resume_model import Resume
from models.resume_section_model import ResumeSection
from models.tag_model import Tag
from models.tag_item_model import TagItem
from models.skill_model import SkillItem
from models.program_contact_model import ProgramContact
from models.session_model import UserSession
from models.opportunity_model import Opportunity
from models.opportunity_app_model import OpportunityApp, ApplicationStage

from .test_api import post_request, POSTS

# This only works because the script is at the top level
from resources.trello_utils import (
    query_board_data,
    Board,
    BoardList,
    Card,
)

REVIEW_BOARDS = {
    'local': '5e3753cdaea77d37fce3496a',
    'dev': '5e39bb0daf879105b1c24462',
    'production': '',
}

LOCAL_OPP_BOARD = '5e4acd35a35ee523c71f9e25'

# TODO: Add trello specific checks
def test_create_program_contact_with_contact(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer test-valid|0123456789',
    }
    with app.test_client() as client:
        response = client.post('/api/contacts/', 
                               data=json.dumps(POSTS['contact']),
                               headers=headers)

        assert response.status_code == 201
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data['id'] is not None
        id_ = data['id']

        program_contacts = Contact.query.get(id_).programs
        assert len(program_contacts) == 1
        assert program_contacts[0].program_id == 1
        assert program_contacts[0].stage == 1
        assert program_contacts[0].program.name == 'Place for Purpose'
        assert program_contacts[0].is_active == True
        assert program_contacts[0].is_approved == False

# TODO: Add trello specific checks
def test_post_contact(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer test-valid|0123456789',
    }
    with app.test_client() as client:
        response = client.post('/api/contacts/', 
                               data=json.dumps(POSTS['contact']),
                               headers=headers)
        assert response.status_code == 201
        set_cookie = response.headers.get('set-cookie')
        assert set_cookie is not None
        assert set_cookie.find('HttpOnly;') is not -1
        # Note: Can't test "secure" due to non-https connection
        contact = Contact.query.filter_by(account_id='test-valid|0123456789').first()
        assert contact.first_name == 'Tester'

        assert UserSession.query.filter_by(contact_id=contact.id).first()

def test_post_formassembly_opportunity_intake(app):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json', 
    }

    card_id = '5e4acdc9ff72ae8a84b4204a'
    board = Board(query_board_data(LOCAL_OPP_BOARD))
    card = board.cards.get(card_id)
    assert card is not None
    card.set_custom_field_values(**{'Opp ID': ''})
    card.move_card(board.lists['stage'][0])

    pprint(card.data)

    gdoc_id = '1b5erb67lgwvxj-g8u2iitvihhti6_nv-7dehdh8ldfw'
    url = '/api/form-assembly/opportunity-app/'
    data = f'google_doc_id={gdoc_id}&org=Balti&title=QA+Tester&salary_lower=50000&salary_upper=60000&google_doc_link=&capabilities%5B0%5D=tfa_16677&capabilities%5B1%5D=tfa_16678&supervisor_first_name=Billy&supervisor_last_name=Daly&supervisor_title=Director+of+Data&supervisor_email=billy%40baltimorecorps.org&supervisor_phone=4436408904&is_supervisor=tfa_16674&race=tfa_16656&gender=tfa_16662&pronouns=tfa_16668&response_id=157007055'

    with app.test_client() as client:
        response = client.post(url, data=data, headers=headers)
        pprint(response.json)
        assert response.status_code == 201
        data = json.loads(response.data)['data']

        assert 'gdoc_id' in data
        assert data['gdoc_id'] == gdoc_id
        assert 'title' in data
        assert data['title'] == 'QA Tester'

        opp = Opportunity.query.filter_by(gdoc_id=gdoc_id).first()
        assert opp is not None
        assert opp.title == 'QA Tester'

        board = Board(query_board_data(LOCAL_OPP_BOARD))
        card = board.cards.get(card_id)
        assert card is not None
        assert card.custom_fields['Opp ID']['value'] == opp.id 
        assert card.stage == 1 


