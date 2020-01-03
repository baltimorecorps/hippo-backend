from flask_restful import Resource, request
#from models.base_model import db
#from models.program_model import Program
#from models.cycle_model import Cycle
#from models.program_contact_model import program_contact
import configparser
import requests

BOARD = '5ddd741f5cc43e2b21346dbb'

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
    url = f"https://api.trello.com/1/boards/{board_id}"
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
def insert_new_card(key, token, card_to_copy):
