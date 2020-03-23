from pprint import pprint
import json

import pytest

from models.contact_model import Contact
from models.experience_model import Experience, Month
from models.resume_model import Resume
from models.resume_section_model import ResumeSection
from models.tag_model import Tag
from models.tag_item_model import TagItem
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
TALENT_INTAKE_BOARDS = {
    'local': '5e37744114d9d01a03ddbcfe',
    'dev': '5e25dae2e640be7e5248a3e6',
    'production': '5ddd741f5cc43e2b21346dbb'
}

TALENT_INTAKE_LABELS = [
    'New', 'Fellowship', 'Mayoral Fellowship', 'PFP', 'PA', 'JHU - Carey'
]

TALENT_INTAKE_ATTACHMENTS = ['Profile', 'Full Response']

def check_labels(board_id, expected_labels):
    board = Board(query_board_data(board_id))
    labels = board.labels['name'].keys()
    print(labels)
    for label in expected_labels:
        assert label in labels

def test_talent_intake_board_labels(app):
    local_board_id = TALENT_INTAKE_BOARDS['local']
    check_labels(local_board_id, TALENT_INTAKE_LABELS)
    prod_board_id = TALENT_INTAKE_BOARDS['production']
    check_labels(prod_board_id, TALENT_INTAKE_LABELS)
    dev_board_id = TALENT_INTAKE_BOARDS['dev']
    check_labels(dev_board_id, TALENT_INTAKE_LABELS)

def test_talent_intake(app):
    mimetype = 'application/x-www-form-urlencoded'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    card_id = '5e4af2d6fc3c0954ff187ddc'

    board_id = TALENT_INTAKE_BOARDS['local']
    board = Board(query_board_data(board_id))
    card = board.cards.get(card_id)
    started_list = board.lists['stage'][1]

    for attachment in TALENT_INTAKE_ATTACHMENTS:
        response = card.remove_attachment(attachment)
    card.set_labels(remove_all=True)
    card.move_card(started_list)

    board = Board(query_board_data(board_id))
    card = board.cards.get(card_id)

    assert card.attachments == {}
    assert card.label_names == []
    assert card.stage == 1

    url = '/api/form-assembly/talent-app/'
    data = (
        'contact_id=123&program_id=1&first_name=Billy&last_name=Daly&email=billy%40example.com&phone=9085784622&street1=2401+Liberty+Heights+Ave&street2=Suite+2730&city=Baltimore&state=MD&postal_code=21215&equity=Race&effectiveness=Effectiveness&programs%5B0%5D=Fellowship&programs%5B1%5D=JHU+-+Carey&programs%5B2%5D=Mayoral+Fellowship&programs%5B3%5D=PFP&programs%5B4%5D=PA&programs%5B5%5D=I%27d+like+some+help+figuring+this+out&mayoral_eligible=Yes&experience=0-2+years&capabilities%5B0%5D=Advocacy+and+Public+Policy&capabilities%5B1%5D=Community+Engagement+and+Outreach&capabilities%5B2%5D=Data+Analysis&capabilities%5B3%5D=Fundraising+and+Development&capabilities%5B4%5D=Marketing+and+Public+Relations&alum_radio=No&race_all=American+Indian+or+Alaskan+Native&gender=Male&pronouns=He%2FHim&response_id=160140910'
    )
    with app.test_client() as client:
        response = client.post(url, data=data, headers=headers)
        pprint(response.json)
        assert response.status_code == 201
        board = Board(query_board_data(board_id))
        card = board.cards.get(card_id)
        assert card.stage == 2
        for label in TALENT_INTAKE_LABELS[1:]:
            assert label in card.label_names
        assert 'Race' in card.desc
        assert '- Data Analysis\n' in card.desc
        assert '0-2 years' in card.desc
        assert '**Mayoral Fellowship:** Yes' in card.desc
        assert '**JHU - Carey:** N/A' in card.desc
        pprint(card.attachments)
        assert card.attachments['Profile']['url'] == (
            'https://app.baltimorecorps.org/profile/123'
        )
        assert card.attachments['Full Response']['url'] == (
            'https://app.formassembly.com/responses/view/160140910'
        )
        data = json.loads(response.data)['data']

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

@pytest.mark.skip
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

    gdoc_id = '1B5ERb67LGwvxJ-g8u2iiTVIhHTi6_nv-7DeHdH8Ldfw'
    url = '/api/form-assembly/opportunity-app/'
    data = f'google_doc_id={gdoc_id}&org=Balti&title=QA+Tester&salary_lower=50000&salary_upper=60000&google_doc_link=&capabilities%5B0%5D=tfa_16677&capabilities%5B1%5D=tfa_16678&supervisor_first_name=Billy&supervisor_last_name=Daly&supervisor_title=Director+of+Data&supervisor_email=billy%40baltimorecorps.org&supervisor_phone=4436408904&is_supervisor=tfa_16674&race=tfa_16656&gender=tfa_16662&pronouns=tfa_16668&response_id=157007055&program_id=1'

    with app.test_client() as client:
        response = client.post(url, data=data, headers=headers)
        pprint(response.json)
        assert response.status_code == 201
        data = json.loads(response.data)['data']

        # assert 'gdoc_id' in data
        # assert data['gdoc_id'] == gdoc_id
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
