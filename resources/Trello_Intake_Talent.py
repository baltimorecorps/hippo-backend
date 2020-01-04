from flask_restful import Resource, request
from models.base_model import db
from models.program_model import Program
from models.cycle_model import Cycle
from models.program_contact_model import ProgramContact
from .ProgramContacts import query_one_program_contact
import configparser
import requests


def get_creds(func):
    def pass_creds_to_func(*args):
        config = configparser.ConfigParser()
        config.read('secrets/trello.cfg')
        key = config['DEFAULT']['TRELLO_API_KEY'],
        token = config['DEFAULT']['TRELLO_API_TOKEN']
        return func(key, token, *args)
    return pass_creds_to_func

def get_intake_talent_board_id(program_id):
    program = Program.query.get(program_id)
    return program.current_cycle.intake_talent_board_id

@get_creds
def query_all_cards(key, token, board_id):
    url = f'https://api.trello.com/1/boards/{board_id}'
    parameters = {'key': key,
                  'token': token,
                  'fields': 'id,name',
                  'cards':'all',
                  'card_fields':'id,name,idList,isTemplate,labels',
                  'card_customFieldItems':'true',
                  'customFields': 'true',
                  'lists': 'all',
                  'list_fields': 'id,name,pos'}
    response = requests.get(url, params=parameters)
    return response.json()

@get_creds
def copy_card(key, token, source_card, target_list, name):
    url = 'https://api.trello.com/1/cards'
    payload = {'key': key,
               'token': token,
               'idList': target_list,
               'idCardSource': source_card,
               'name': name,
               'keepFromSource': 'all'}
    response = requests.post(url, data=payload)
    return response.json()

@get_creds
def set_custom_field(key, token, card_id, field_id, value='', value_id=''):
    url = f'https://api.trello.com/1/card/{card_id}/customField/{field_id}/item'
    payload = {'idValue': value_id,
               'value': value,
               'key': key,
               'token': token}
    response = requests.put(url, json=payload)
    return response.json()



class IntakeTalentBoard(Resource):

    def get(self, program_id):
        board_id = get_intake_talent_board_id(program_id)
        return {'status': 'success', 'data': board_id}, 200

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

        template_id = '5e0d2fce847bc22ccf95e67e'
        target_list = '5ddd7432fbe0215a8b7c5494'

        new_card = copy_card(template_id, target_list,
                             f'{contact.first_name} {contact.last_name}')

        return {'status': 'success', 'data': new_card}, 201
