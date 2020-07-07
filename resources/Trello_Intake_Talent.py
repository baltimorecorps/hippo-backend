from flask_restful import Resource, request
from models.base_model import db
from models.program_model import Program
from models.program_contact_model import ProgramContact, ProgramContactSchema
from .ProgramContacts import query_one_program_contact
from .trello_utils import (
    query_board_data,
    update_card,
    Board,
    Card,
    BoardList
)


program_contact_schema = ProgramContactSchema()

def get_intake_talent_board_id(program_id):
    program = Program.query.get(program_id)
    return program.trello_board_id

BOARD_ID = '5ddd741f5cc43e2b21346dbb'

def add_new_talent_card(contact_id, program_id=1):
    board_id = get_intake_talent_board_id(program_id)
    program_contact = query_one_program_contact(contact_id, program_id)
    contact = program_contact.contact
    email = contact.email_primary.email

    board_data = query_board_data(board_id)
    board = Board(board_data)
    started_list = board.lists['stage'][1]
    existing_card = board.find_card_by_custom_field('Email', email)
    fields_data = {
        'Phone': contact.phone_primary,
        'Email': email,
        'External ID': str(program_contact.id)
    }
    if existing_card:
        existing_card.set_custom_field_values(**fields_data)
        result = existing_card.move_card(started_list)
        program_contact.update(**{'card_id': existing_card.id})
    else:
        card_data = {
            'name': f'{contact.first_name} {contact.last_name}'
        }
        new_card = started_list.add_card_from_template(**card_data)
        program_contact.update(**{'card_id': new_card.id})
        result = new_card.set_custom_field_values(**fields_data)
    result['program_contact'] = program_contact_schema.dump(program_contact)
    return result

class IntakeTalentBoard(Resource):

    def get(self, program_id):
        board_id = get_intake_talent_board_id(program_id)
        data = query_board_data(board_id)
        board = Board(data)
        members = board.cards[0].data['idMembers']
        return {'status': 'success', 'data': members}, 200

    def put(self, program_id):
        board_id = get_intake_talent_board_id(program_id)
        return {'status': 'success', 'hi': board_id}, 200

class IntakeTalentCard(Resource):

    def get(self, contact_id, program_id):
        result = add_new_talent_card(contact_id, program_id)
        return {'status': 'success', 'data': result}, 200

    def post(self, contact_id, program_id):
        result = add_new_talent_card(contact_id, program_id)
        return {'status': 'success', 'data': result}, 201
