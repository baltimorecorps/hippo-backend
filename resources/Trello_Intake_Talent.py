from flask_restful import Resource, request
from models.base_model import db
from models.program_model import Program
from models.cycle_model import Cycle
from models.program_contact_model import ProgramContact
from .ProgramContacts import query_one_program_contact
from .trello_utils import (
    query_board_data,
    Board,
    Card,
    BoardList
)
import configparser
import requests

def get_intake_talent_board_id(program_id):
    program = Program.query.get(program_id)
    return program.current_cycle.intake_talent_board_id

BOARD_ID = '5ddd741f5cc43e2b21346dbb'

class IntakeTalentBoard(Resource):

    def get(self, program_id):
        board_id = get_intake_talent_board_id(program_id)
        data = query_board_data(BOARD_ID)
        board = Board(data)
        return {'status': 'success', 'data': board.lists['stage'][1].template.name}, 200

    def put(self, program_id):
        board_id = get_intake_talent_board_id(program_id)
        return {'status': 'success', 'hi': board_id}, 200

class IntakeTalentCard(Resource):

    def get(self, contact_id, program_id):
        board_id = get_intake_talent_board_id(program_id)
        program_contact = query_one_program_contact(contact_id, program_id)
        contact = program_contact.contact

        data = {
            'board_id': board_id,
            'program_contact_id': program_contact.id,
            'contact_id': contact.first_name
        }
        return {'status': 'success', 'data': data}, 200

    def post(self, contact_id, program_id):
        board_id = get_intake_talent_board_id(program_id)
        program_contact = query_one_program_contact(contact_id, program_id)
        contact = program_contact.contact

        data = query_board_data(BOARD_ID)
        board = Board(data)
        started_list = board.lists['stage'][1]
        data = {'name': f'{contact.first_name} {contact.last_name}'}
        new_card = started_list.add_card_from_template(**data)
        return {'status': 'success', 'data': new_card.list.id}, 201
