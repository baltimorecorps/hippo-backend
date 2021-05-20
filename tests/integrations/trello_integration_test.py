from pprint import pprint
import json

import pytest

from app.models.contact_model import Contact
from app.models.experience_model import Experience, Month
from app.models.session_model import UserSession
from app.models.base_model import db

from tests.api_tests.test_api import post_request, POSTS

# This only works because the script is at the top level
from app.resources.trello_utils import (
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
