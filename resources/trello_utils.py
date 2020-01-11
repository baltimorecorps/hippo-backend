import configparser
import requests
import operator as op


# general methods
def get_creds(func):
    def pass_creds_to_func(*args, **kwargs):
        config = configparser.ConfigParser()
        config.read('secrets/trello.cfg')
        key = config['DEFAULT']['TRELLO_API_KEY'],
        token = config['DEFAULT']['TRELLO_API_TOKEN']
        return func(key, token, *args, **kwargs)
    return pass_creds_to_func

@get_creds
def query_board_data(key, token, board_id):
    '''
    api docs: https://developers.trello.com/reference#boardsboardid-1
    '''
    url = f'https://api.trello.com/1/boards/{board_id}'
    querystring = {'key': key,
                   'token': token,
                   'fields': 'id,name',
                   'cards':'all',
                   'card_fields':'id,name,idList,isTemplate,labels,closed,desc',
                   'card_customFieldItems':'true',
                   'customFields': 'true',
                   'lists': 'all',
                   'list_fields': 'id,name,pos',
                   'labels': 'all',
                   'label_fields': 'name'}
    response = requests.get(url, params=querystring)
    return response.json()

@get_creds
def query_checklists(key, token, card_id):
    '''
    api-doc: https://developers.trello.com/reference#cardsidchecklists
    '''
    url = f'https://api.trello.com/1/cards/{card_id}/checklists'
    querystring = {'key': key,
                   'token': token,
                   'checkItems':'all',
                   'checkItem_fields':'name,state',
                   'filter':'all',
                   'fields':'name,idCard',}
    response = requests.get(url, params=querystring)
    return response.json()

@get_creds
def query_card(key, token, card_id, **card_params):
    '''
    api_docs: https://developers.trello.com/reference#cardsid-1
    '''
    url = f'https://api.trello.com/1/cards/{card_id}'
    querystring = {'key': key,
                   'token': token,
                   'fields': 'id,name,idList,isTemplate,labels,closed,desc'}
    response = requests.get(url, params=querystring)
    return response.json()

@get_creds
def insert_card(key, token, **card_data):
    '''
    api_docs: https://developers.trello.com/reference#cardsid-1
    '''
    url = 'https://api.trello.com/1/cards'
    payload = {'key': key,
               'token': token,
               **card_data}
    response = requests.post(url, data=payload)
    return response.json()

@get_creds
def update_custom_field_val(key, token, card_id, field_id, value='', value_id=''):
    '''
    api docs: https://developers.trello.com/reference#customfielditemsid
    '''
    url = f'https://api.trello.com/1/card/{card_id}/customField/{field_id}/item'
    payload = {'key': key,
               'token': token,
               'value': value,
               'idValue': value_id}
    response = requests.put(url, json=payload)
    return response.json()

@get_creds
def update_card(key, token, card_id, **new_values):
    url = f'https://api.trello.com/1/card/{card_id}'
    payload = {'key': key,
               'token': token,
               **new_values}
    response = requests.put(url, data=payload)
    return response.json()

@get_creds
def insert_checklist(key, token, card_id, **checklist_data):
    '''
    api docs: https://developers.trello.com/reference/#checklists
    '''
    url = 'https://api.trello.com/1/checklists'
    payload = {'key': key,
               'token': token,
               'idCard': card_id,
               **checklist_data}
    response = requests.post(url, data=payload)
    return response.text

@get_creds
def insert_checklist_item(key, token, checklist_id, name, **item_data):
    '''
    api docs: https://developers.trello.com/reference/#checklistsidcheckitems
    '''
    url = f'https://api.trello.com/1/checklists/{checklist_id}/checkItems'
    payload = {'key': key,
               'token': token,
               'name': name,
               **item_data}
    response = requests.post(url, data=payload)
    return response.text

# classes
class Board(object):
    def __init__(self, data):
        self.data = data
        self.id = data['id']
        self.lists = {'stage': {}, 'id': {}}
        self.custom_fields = {'id': {}, 'name': {}}
        self.cards = []

        self.parse_custom_fields()
        self.parse_lists()
        self.parse_cards()

    def parse_lists(self):
        sorted(self.data['lists'], key=op.itemgetter('pos'))
        for i, board_list in enumerate(self.data['lists']):
            _list = BoardList(board_list, i, self)
            self.lists['stage'][i] = _list
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
        for f in self.data['customFields']:
            field = CustomField(f, self)
            self.custom_fields['id'][field.id] = field
            self.custom_fields['name'][field.name] = field

    def find_card_by_custom_field(self, field, value, many=False):
        cards = [card for card in self.cards
                 if card.custom_fields
                 and card.custom_fields[field]['value']==value]
        if not cards:
            return None
        elif many:
            return cards
        else:
            return cards[0]
            
class CustomField(object):
    def __init__(self, data, board):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.options = {}

        self.board = board

        self.parse_options(data)

    def parse_options(self, data):
        if self.type=='list':
            self.options = {'val': {}, 'id': {}}
            for option in data['options']:
                val = option['value']['text']
                _id = option['id']
                self.options['val'][val] = _id
                self.options['id'][_id] = val

    def format_update(self, new_value):
        updates = {'value': '', 'value_id': ''}
        if self.type=='list':
            updates['value_id'] = self.options['val'][new_value]
        else:
            updates['value'] = {self.type: new_value}
        return updates

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

    def add_card_from_template(self, **data):
        card_data = {
            'idList': self.id,
            'idCardSource': self.template.id,
            'keepFromSource': 'checklists,members,due,labels',
            **data
        }
        result = insert_card(**card_data)
        new_card = Card(result, self.board)
        new_card.list = self
        return new_card

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
        field_items = self.data.get('customFieldItems')
        if field_items:
            for item in field_items:
                field = self.get_custom_field_by_id(item['idCustomField'])
                if field.type=='list':
                    val = field.options['id'][item['idValue']]
                else:
                    val = item['value'][field.type]
                self.custom_fields[field.name] = {
                    'id': item['id'],
                    'value': val,
                    'field': field
                }

    def get_custom_field_by_id(self, field_id):
        return self.board.custom_fields['id'][field_id]

    def get_custom_field_by_name(self, name):
        return self.board.custom_fields['name'][name]

    def get_checklists(self):
        self.checklists = {}
        data = query_checklists(self.id)
        for checklist in data:
            self.checklists[checklist['name']] = {
                'id': checklist['id'],
                'items': checklist['checkItems']
            }
    def update_checklist_from_template(self, template_card):
        pass
        #self.get_checklists()
        #template_card.get_checklists()
        #checklists_to_add = {}
        #items_to_add = {}

    def update_custom_field_val(self, field_name, value):
        field = self.custom_fields[field_name]['field']
        update = field.format_update(value)
        set_custom_field_val(self.id, field.id, update['value'], update['value_id'])
