import configparser
import requests
import operator as op


# general methods
def get_creds(func):
    def pass_creds_to_func(*args):
        config = configparser.ConfigParser()
        config.read('secrets/trello.cfg')
        key = config['DEFAULT']['TRELLO_API_KEY'],
        token = config['DEFAULT']['TRELLO_API_TOKEN']
        return func(key, token, *args)
    return pass_creds_to_func

@get_creds
def query_board_data(key, token, board_id):
    url = f'https://api.trello.com/1/boards/{board_id}'
    parameters = {'key': key,
                  'token': token,
                  'fields': 'id,name',
                  'cards':'all',
                  'card_fields':'id,name,idList,isTemplate,labels,closed,desc',
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


# classes
class Board(object):
    def __init__(self, data):
        self.data = data
        self.id = data['id']
        self.lists = {'index': {}, 'id': {}}
        self.custom_fields = {}
        self.cards = []

        self.parse_custom_fields()
        self.parse_lists()
        self.parse_cards()

    def parse_lists(self):
        sorted(self.data['lists'], key=op.itemgetter('pos'))
        for i, board_list in enumerate(self.data['lists']):
            _list = BoardList(board_list, i, self)
            self.lists['index'][i] = _list
            self.lists['id'][_list.id] = _list

    def parse_cards(self):
        for c in self.data['cards']:
            _card = Card(c, self)
            _list = self.lists['id'][_card.idList]
            _card.list = _list
            self.cards.append(_card)

            if _card.data['isTemplate']==True:
                _list.template = _card
            else:
                self.lists['id'][_card.idList].cards.append(_card)

    def parse_custom_fields(self):
        fields = self.custom_fields
        for f in self.data['customFields']:
            fields[f['id']] = {
                'name': f['name'],
                'type': f['type'],
            }
            if f['type']=='list':
                fields[f['id']]['options'] = {'val': {}, 'id': {}}
                for option in f['options']:
                    val = option['value']['text']
                    _id = option['id']
                    fields[f['id']]['options']['val'][val] = _id
                    fields[f['id']]['options']['id'][_id] = val

class BoardList(object):
    def __init__(self, data, index, board):
        self.id = data['id']
        self.name = data['name']
        self.stage = index

        self.board = board
        self.template = None
        self.cards = []

        @property
        def active_cards(self):
            return [card for card in self.cards if not card.closed]

        @property
        def inactive_cards(self):
            return [card for card in self.cards if card.closed]

class Card(object):
    def __init__(self, data, board):
        self.data = data
        self.id = data['id']
        self.name = data['name']
        self.idList = data['idList']
        self.closed = data['closed']
        self.desc = data['desc']
        self.custom_fields = {}

        self.board = board
        self.list = None

        self.parse_custom_field_items()

    def parse_custom_field_items(self):
        fields = self.custom_fields
        if self.data['customFieldItems']:
            for f in self.data['customFieldItems']:
                field = self.board.custom_fields[f['idCustomField']]
                if field['type']=='list':
                    val = field['options']['id'][f['idValue']]
                else:
                    val = f['value'][field['type']]
                fields[field['name']] = {
                    'id': f['id'],
                    'field_id': f['idCustomField'],
                    'type': field['type'],
                    'value': val
                }
