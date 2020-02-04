import configparser
import requests
import operator as op
from flask import current_app

CARD_FIELDS = 'id,name,idMembers,idList,isTemplate,labels,closed,desc'

# general methods
def get_creds(func):
    def pass_creds_to_func(*args, **kwargs):
        config = current_app.config
        key = config['TRELLO_API_KEY']
        token = config['TRELLO_API_TOKEN']
        return func(key, token, *args, **kwargs)
    return pass_creds_to_func

@get_creds
def query_board_data(key, token, board_id, card_fields=CARD_FIELDS):
    '''
    api docs: https://developers.trello.com/reference#boardsboardid-1
    '''
    url = f'https://api.trello.com/1/boards/{board_id}'
    querystring = {'key': key,
                   'token': token,
                   'fields': 'id,name',
                   'cards':'all',
                   'card_fields': card_fields,
                   'card_customFieldItems':'true',
                   'customFields': 'true',
                   'lists': 'all',
                   'list_fields': 'id,name,pos',
                   'labels': 'all',
                   'label_fields': 'name'}
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
def query_card(key, token, card_id, **card_params):
    '''
    api_docs: https://developers.trello.com/reference#cardsid-1
    '''
    url = f'https://api.trello.com/1/cards/{card_id}'
    querystring = {'key': key,
                   'token': token,
                   'fields': 'id,name,idList,isTemplate,labels,closed,desc',
                   'customFieldItems': 'true',
                   'checklists': 'all',
                   'checklist_fields': 'id, name',
                   'checkItems':'all',
                   'checkItem_fields':'name,state',
                   **card_params}
    response = requests.get(url, params=querystring)
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
    return response.text

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
def delete_checklist(key, token, card_id, checklist_id):
    '''
    api docs: https://developers.trello.com/reference/#cardsidchecklistsidchecklist
    '''
    url = f'https://api.trello.com/1/cards/{card_id}/checklists/{checklist_id}'
    querystring = {"key": key,
                   "token": token}
    response = requests.delete(url, params=querystring)
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

@get_creds
def update_checklist_item(key, token, card_id, item_id, **item_data):
    '''
    api docs: https://developers.trello.com/reference/#cardsidcheckitemidcheckitem-1
    '''
    url = f'https://api.trello.com/1/cards/{card_id}/checkItem/{item_id}'
    payload = {'key': key,
               'token': token,
               **item_data}
    response = requests.put(url, data=payload)
    return response.text

@get_creds
def delete_checklist_item(key, token, card_id, checklist_item_id):
    '''
    api docs: https://developers.trello.com/reference/#cardsidcheckitemidcheckitem-2
    '''
    url = f'https://api.trello.com/1/cards/{card_id}/checklists/{checklist_item_id}'
    querystring = {"key": key,
                   "token": token}
    response = requests.delete(url, params=querystring)
    return response.text

# classes
class Board(object):
    def __init__(self, data):
        self.data = data
        self.id = data['id']
        self.lists = {'stage': {}, 'id': {}}
        self.custom_fields = {'id': {}, 'name': {}}
        self.cards = {}
        self.labels = {'id': {}, 'name': {}}

        self.parse_custom_fields()
        self.parse_lists()
        self.parse_cards()
        self.parse_labels()

    def parse_lists(self):
        sorted(self.data['lists'], key=op.itemgetter('pos'))
        for i, board_list in enumerate(self.data['lists']):
            list_ = BoardList(board_list, i, self)
            self.lists['stage'][i] = list_
            self.lists['id'][list_.id] = list_

    def parse_cards(self):
        for c in self.data['cards']:
            card = Card(c, self)
            list_ = self.lists['id'][card.idList]
            card.list = list_
            self.cards[card.id] = card

            if card.data['isTemplate']==True:
                list_.template = card
            else:
                self.lists['id'][card.idList].cards.append(card)

    def parse_custom_fields(self):
        for f in self.data['customFields']:
            field = CustomField(f, self)
            self.custom_fields['id'][field.id] = field
            self.custom_fields['name'][field.name] = field

    def parse_labels(self):
        labels = self.data.get('labels')
        for label in labels:
            name = label['name']
            _id = label['id']
            if name:
                self.labels['name'][name] = _id
                self.labels['id'][_id] = name

    def find_card_by_custom_field(self, field, value, many=False):
        cards = [card for card in self.cards.values()
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
        return [card for card in self.cards if not card.archived]

    @property
    def inactive_cards(self):
        return [card for card in self.cards if card.archived]

    def add_card_from_template(self, **data):
        card_data = {
            'idList': self.id,
            'idCardSource': self.template.id,
            'keepFromSource': 'all',
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
        self.archived = data['closed']
        self.desc = data['desc']
        self.custom_fields = {}

        self.board = board
        self.list = None

        self.parse_custom_field_items()

    @property
    def stage(self):
        return self.list.stage

    def parse_custom_field_items(self):
        custom_fields = self.board.custom_fields['id'].values()
        card_fields = self.data.get('customFieldItems')
        if card_fields:
            card_fields = {f['idCustomField']: f for f in card_fields}
        else:
            card_fields = {}
        for field in custom_fields:
            val = None
            card_field_id = None
            if field.id in card_fields.keys():
                card_field = card_fields[field.id]
                card_field_id = card_field['id']
                if field.type=='list':
                    val = field.options['id'][card_field['idValue']]
                else:
                    val = card_field['value'][field.type]
            self.custom_fields[field.name] = {
                'id': card_field_id,
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
        return self.checklists

    def add_missing_checklists(self, current_checklists, template_checklists):
        to_add = []
        for name, checklist in template_checklists.items():
            if name not in current_checklists.keys():
                data = {'idChecklistSource': checklist['id']}
                insert_checklist(self.id, **data)

    def add_missing_checklist_items(self, current_checklists, template_checklists):
        for name, checklist in template_checklists.items():
            current_checklist = current_checklists.get(name)
            template_items = checklist['items']
            if current_checklist and template_items:
                current_id = current_checklist['id']
                if current_checklist['items']:
                    current_items = [item['name'] for item in current_checklist['items']]
                else:
                    current_items = []
                for item in template_items:
                    if item['name'] not in current_items:
                        insert_checklist_item(current_id, item['name'])

    def update_checklists_from_template(self, template_card):
        current = self.get_checklists()
        template = template_card.get_checklists()

        self.add_missing_checklists(current, template)
        self.add_missing_checklist_items(current, template)

    def set_custom_field_values(self, **fields_dict):
        for field_name, val in fields_dict.items():
            field = self.custom_fields[field_name]['field']
            update = field.format_update(val)
            update_custom_field_val(self.id, field.id,
                                    update['value'], update['value_id'])
        result = query_card(self.id)
        return result


    def move_card(self, new_list):
        template = new_list.template
        data = {
            'idList': new_list.id
        }
        update_card(self.id, **data)
        self.update_checklists_from_template(template)
        result = query_card(self.id)
        return result

    def complete_checklist_items(self):
        checklists = self.get_checklists()
        for checklist in checklists.values():
            items = checklist['items']
            if items:
                for item in items:
                    data = {'state': 'complete'}
                    update_checklist_item(self.id, item['id'], **data)
        result = query_card(self.id)
        return result
