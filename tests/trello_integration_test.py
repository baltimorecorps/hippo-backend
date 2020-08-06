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

from .test_api import post_request, POSTS

# This only works because the script is at the top level
from resources.trello_utils import (
    query_board_data,
    Board,
    BoardList,
    Card,
)

TALENT_INTAKE_BOARDS = {
    'local': '5e37744114d9d01a03ddbcfe',
    'dev': '5e25dae2e640be7e5248a3e6',
    'production': '5ddd741f5cc43e2b21346dbb'
}

TALENT_INTAKE_LABELS = [
    'New', 'Fellowship', 'Mayoral Fellowship', 'PFP', 'PA', 'JHU - Carey'
]

TALENT_INTAKE_ATTACHMENTS = ['Profile', 'Full Response']

LABELS = ['New', 'PFP']

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

    contact = Contact.query.get(123)
    board_id = TALENT_INTAKE_BOARDS['local']
    board = Board(query_board_data(board_id))
    card = board.cards.get(card_id)
    started_list = board.lists['stage'][1]

    for attachment in TALENT_INTAKE_ATTACHMENTS:
        response = card.remove_attachment(attachment)
    card.set_labels(label_names=['New', 'Fellowship'])
    card.move_card(started_list)

    board = Board(query_board_data(board_id))
    card = board.cards.get(card_id)

    assert card.attachments == {}
    assert card.label_names == ['New', 'Fellowship']
    assert card.stage == 1
    assert contact.stage == 1

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
        contact = Contact.query.get(123)
        assert card.stage == 2
        assert contact.stage == 2
        assert 'New' in card.label_names
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

def test_resubmit_approved_app(app):
    mimetype = 'application/x-www-form-urlencoded'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    card_id = '5e4af2d6fc3c0954ff187ddc'

    board_id = TALENT_INTAKE_BOARDS['local']
    board = Board(query_board_data(board_id))
    card = board.cards.get(card_id)
    approved_list = board.lists['stage'][3]
    card.move_card(approved_list)

    board = Board(query_board_data(board_id))
    card = board.cards.get(card_id)
    assert card.stage == 3

    url = '/api/form-assembly/talent-app/'
    data = (
        'contact_id=123&program_id=1&first_name=Billy&last_name=Daly&email=billy%40example.com&phone=9085784622&street1=2401+Liberty+Heights+Ave&street2=Suite+2730&city=Baltimore&state=MD&postal_code=21215&equity=Race&effectiveness=Effectiveness&programs%5B0%5D=Fellowship&programs%5B1%5D=JHU+-+Carey&programs%5B2%5D=Mayoral+Fellowship&programs%5B3%5D=PFP&programs%5B4%5D=PA&programs%5B5%5D=I%27d+like+some+help+figuring+this+out&mayoral_eligible=Yes&experience=0-2+years&capabilities%5B0%5D=Advocacy+and+Public+Policy&capabilities%5B1%5D=Community+Engagement+and+Outreach&capabilities%5B2%5D=Data+Analysis&capabilities%5B3%5D=Fundraising+and+Development&capabilities%5B4%5D=Marketing+and+Public+Relations&alum_radio=No&race_all=American+Indian+or+Alaskan+Native&gender=Male&pronouns=He%2FHim&response_id=160140910'
    )

    with app.test_client() as client:
        response = client.post(url, data=data, headers=headers)
        pprint(response.json)
        assert response.status_code == 400
        message = json.loads(response.data)['message']
        assert message == 'Application has already been submitted'

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
        assert contact.email == 'testerb@example.com'
        assert contact.profile.years_exp is None
        assert contact.card_id == '5e6fc5ebab29b671c997828c'

        assert UserSession.query.filter_by(contact_id=contact.id).first()

# TODO: Add trello specific checks
def test_post_duplicate_contact(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer test-valid|0123456789abcdefabcdefff',
    }

    contact_data = POSTS['contact'].copy()
    contact_data['account_id'] = 'test-valid|0123456789abcdefabcdefff'

    with app.test_client() as client:
        response = client.post('/api/contacts/',
                               data=json.dumps(contact_data),
                               headers=headers)
        assert response.status_code == 400
        message = json.loads(response.data)['message']
        assert message == 'A contact with this account already exists'

def test_submit_profile(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    card_id = '5e4af2d6fc3c0954ff187ddc'

    contact = Contact.query.get(123)
    board_id = TALENT_INTAKE_BOARDS['local']
    board = Board(query_board_data(board_id))
    card = board.cards.get(card_id)
    started_list = board.lists['stage'][1]

    for attachment in TALENT_INTAKE_ATTACHMENTS:
        response = card.remove_attachment(attachment)
    card.set_labels(label_names=['New', 'Fellowship'])
    card.move_card(started_list)

    board = Board(query_board_data(board_id))
    card = board.cards.get(card_id)

    assert card.attachments == {}
    assert card.label_names == ['New', 'Fellowship']
    assert card.stage == 1
    assert contact.stage == 1



    with app.test_client() as client:
        response = client.post('/api/contacts/123/submit',
                               data={},
                               headers=headers)
        pprint(response.json)
        assert response.status_code == 201

        board = Board(query_board_data(board_id))
        card = board.cards.get(card_id)
        contact = Contact.query.get(123)

        assert contact.stage == 2
        assert 'New' in card.label_names
        for label in LABELS:
            assert label in card.label_names
        assert 'Test response' in card.desc
        assert '- Data Analysis\n' in card.desc
        assert '3-5' in card.desc
        assert card.attachments['Profile']['url'] == (
            'https://app.baltimorecorps.org/profile/123'
        )

        data = response.json['data']
        assert data['instructions']['submit']
