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
from models.base_model import db

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
    email = contact.email_main
    contact.stage = 1
    db.session.commit()
    board_id = TALENT_INTAKE_BOARDS['local']
    board = Board(query_board_data(board_id))
    card = board.find_card_by_custom_field('Email', email)
    if card:
        response = card.delete()
        assert response.status_code == 200

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
        card = board.find_card_by_custom_field('Email', email)
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
        assert card.custom_fields['Email']['value'] == email
        data = json.loads(response.data)['data']

        #check that the card id was set
        contact = Contact.query.get(123)
        card_id = contact.card_id
        assert card_id is not None


def test_resubmit_approved_app(app):
    mimetype = 'application/x-www-form-urlencoded'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    board_id = TALENT_INTAKE_BOARDS['local']
    board = Board(query_board_data(board_id))
    card = board.find_card_by_custom_field('Email', 'billy@example.com')
    assert card is not None

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

def test_submit_profile(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
    }

    card_id = '5e4af2d6fc3c0954ff187ddc'

    contact = Contact.query.get(123)
    email = contact.email_main
    contact.stage = 1
    db.session.commit()
    board_id = TALENT_INTAKE_BOARDS['local']
    board = Board(query_board_data(board_id))
    card = board.find_card_by_custom_field('Email', email)
    if card:
        response = card.delete()
        assert response.status_code == 200

    contact = Contact.query.get(123)
    assert contact.stage == 1



    with app.test_client() as client:
        response = client.post('/api/contacts/123/profile/submit',
                               data={},
                               headers=headers)
        pprint(response.json)
        assert response.status_code == 201

        board = Board(query_board_data(board_id))
        card = board.find_card_by_custom_field('Email', email)
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
        assert card.custom_fields['Email']['value'] == email

        data = response.json['data']
        assert data['instructions']['submit']

        #check that the card id was set
        contact = Contact.query.get(123)
        card_id = contact.card_id
        assert card_id is not None

        # Check that the card is deleted
        card.delete()
        board = Board(query_board_data(board_id))
        card = board.cards.get(card_id)
        assert card is None
