from __future__ import print_function
import sys
import pickle
import os
import os.path
import json
from enum import Enum
from collections import defaultdict
from pprint import pprint

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive'
]

# The ID of a sample document:
# https://docs.google.com/document/d/1RExcI9pWu6JTGqHDtXzfF0hnOj0U4KQtKf4qpFzXfwE/edit
DOCUMENT_ID = '1RExcI9pWu6JTGqHDtXzfF0hnOj0U4KQtKf4qpFzXfwE'
SECTIONS = [
    {'row': 1, 'col': 0, 'name': 'Relevant Experience', 'shape': (1,1)},
    {'row': 1, 'col': 1, 'name': 'Skills and Abilities', 'shape': (1,2)},
    {'row': 1, 'col': 1, 'name': 'Achievements', 'shape': (1,2)},
    {'row': 1, 'col': 1, 'name': 'Relevant Education', 'shape': (1,2)},
    {'row': 2, 'col': 0, 'name': 'Additional Experience', 'shape': (1,1)},
    {'row': 2, 'col': 1, 'name': 'Additional Education', 'shape': (1,2)},
    {'row': 2, 'col': 1, 'name': 'Other Achievements', 'shape': (1,2)},
    {'row': 2, 'col': 1, 'name': 'Additional Skills', 'shape': (1,2)},
    {'row': 2, 'col': 1, 'name': 'Languages', 'shape': (1,2)},
]

def get_user_creds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../secrets/gdoc-creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def get_service_creds():
    try:
        acct_info = json.loads(os.environ.get('GOOGLE_SERVICE_ACCT_KEY'))
        credentials = service_account.Credentials.from_service_account_info(
            acct_info)
    except TypeError:
        credentials = service_account.Credentials.from_service_account_file(
            'secrets/HippoSvcAcctDev.json')
    return credentials.with_scopes(SCOPES)

def init_services():
    creds = get_service_creds()
    gdrive = build('drive', 'v3', credentials=creds)
    gdocs = build('docs', 'v1', credentials=creds)

    return (gdrive, gdocs)

def dump_document(doc_id):
    (gdrive, gdocs) = init_services()
    document = gdocs.documents().get(documentId=doc_id).execute()
    print(json.dumps(document))

def make_replace_request(item):
    (key, value) = item
    return {
        'replaceAllText': {
            'containsText': {
                'text': f'[[{key}]]',
                'matchCase': 'true'
            },
            'replaceText': value
        }
    }

def make_insert_text_request(text, location):
    return {
        'insertText': {
            'text': text,
            'location': {
                'segmentId': '',
                'index': location,
            }
        }
    }

def make_insert_table_request(location, rows, cols):
    return {
        'insertTable': {
            'rows': rows,
            'columns': cols,
            'location': {
                'segmentId': '',
                'index': location,
            }
        }
    }

def make_delete_table_row_request(location, row):
    return {
        'deleteTableRow': {
            'tableCellLocation': {
                'tableStartLocation': {
                    'segmentId': '',
                    'index': location,
                },
                'rowIndex': row,
                'columnIndex': 0,
            }
        }
    }

def make_table_cell_style_request(style, location, row, col):
    return {
        'updateTableCellStyle': {
            'tableCellStyle': style,
            'fields': '*',
            'tableRange': {
                'tableCellLocation': {
                    'tableStartLocation': {
                        'segmentId': '',
                        'index': location,
                    },
                    'rowIndex': row,
                    'columnIndex': col,
                },
                'rowSpan': 1,
                'columnSpan': 1,
            }
        }
    }

def make_text_style_request(obj, offset):
    return {
        'updateTextStyle': {
            'textStyle': obj['style'],
            'fields': '*',
            'range': {
                'segmentId': '',
                'startIndex': obj['start'] + offset,
                'endIndex': obj['end'] + offset,
            },
        }
    }

def make_paragraph_style_request(obj, offset):
    return {
        'updateParagraphStyle': {
            'paragraphStyle': obj['style'],
            'fields': '*',
            'range': {
                'segmentId': '',
                'startIndex': obj['start'] + offset,
                'endIndex': obj['end'] + offset,
            },
        }
    }

def get_update_index(update):
    key = list(update.keys())[0]
    if key == 'deleteTableRow':
        return update[key]['tableCellLocation']['tableStartLocation']['index']
    elif key == 'updateTableCellStyle':
        return update[key]['tableRange']['tableCellLocation']['tableStartLocation']['index']
    elif key in ('updateTextStyle', 'updateParagraphStyle'):
        return update[key]['range']['startIndex']
    elif key in ('insertText', 'insertTable'):
        return update[key]['location']['index']
    elif key == 'replaceAllText':
        return 0
    else:
        assert False, f'Got unexpected update type {key}'

def order_updates(updates):
    # See https://developers.google.com/docs/api/how-tos/best-practices#edit_backwards_for_efficiency
    def sort_fn(update):
        key = list(update.keys())[0]
        return get_update_index(update)

    return sorted(updates, key=sort_fn, reverse=True)


def get_tables(elements):
    tables = []
    for elem_index, element in enumerate(elements):
        if 'table' in element:
            tables.append((elem_index, element))
    return tables


class DocState(Enum):
    UPDATE_CONTACT_INFO = 1
    PARSE_TEMPLATE = 2
    INSERT_TEMPLATE_TEXT = 3
    STYLE_TEMPLATE_ENTRIES = 4
    INSERT_CONTENT = 5

class Layout(object):
    def __init__(self):
        # This is our representation of the 'main grid' that divides up
        # the whole document. Using (row, col) pairs as keys, we will note
        # which Sections are stored in which grid square, which will allow
        # us to keep track of where everthing is
        self.main_grid = defaultdict(list)

        self.sections = {}

    def add_section(self, row, col, section):
        self.main_grid[(row, col)].append(section)
        self.sections[section.name] = section

    def get_section(self, name):
        return self.sections[name]

    def generate_entries(self, num_entries):
        entries = []
        for key, n in num_entries.items():
            entries.extend(self.get_section(key).generate_entries(n))
        return entries

    def generate_style_updates(self):
        updates = []
        for section in self.sections.values():
            updates.extend(section.generate_style_updates())
        return updates

    def generate_insert_text_updates(self):
        updates = []
        for section in self.sections.values():
            updates.extend(section.generate_insert_text_updates())
        return updates

    def parse(self, document, doc_state):
        body_content = document['body']['content']
        tables = get_tables(body_content)
        # We assume the first table is the main grid, this is kind of brittle
        # but we'll see if we need to make it any better
        assert len(tables) > 0
        main_grid_table = tables[0][1]

        def get_main_grid_cell(row, col):
            return main_grid_table['table']['tableRows'][row]['tableCells'][col]

        for rc, sections in self.main_grid.items():
            row, col = rc
            container = get_main_grid_cell(row, col)
            curr_index = 0
            for section in sections:
                # This will populate the section objects with the relevant
                # information
                curr_index = section.parse(doc_state, container, curr_index)

class DocumentParseError(Exception):
    pass

class Template(object):
    def __init__(self):
        self.text = ''
        self.cell_style = {}
        self.paragraph_styles = []
        self.text_styles = []

class Section(object):
    def __init__(self, name, shape=(1,1)):
        self.name = name
        # Every section starts with a template entry, so this starts at 1
        self.num_items = 1
        self.container = None

        # Entry shape is the # of (rows, columns) in the tables that make up
        # each entry in this section
        self.entry_shape = shape

        # Every cell in the entry will have a template, indexed by its
        # (row, col) position
        self.templates = {}

        # Keep track of whether or not we've generated the entries for our
        # section yet, to ensure it happens for all sections before we try
        # and parse any 'updated' documents (e.g. in state INSERT_TEMPLATE_TEXT
        # or later)
        self.generated_entries = False

    def parse(self, doc_state, container, start_index):
        end_index = self._parse_structure(container, start_index)
        if doc_state == DocState.PARSE_TEMPLATE:
            self._parse_template_content()
        elif doc_state in (DocState.INSERT_TEMPLATE_TEXT,
                           DocState.STYLE_TEMPLATE_ENTRIES):
            if not self.generated_entries:
                raise DocumentParseError(
                    f'Invalid parse in state {doc_state}: {self.name} has not yet generated entries')
        else:
            raise DocumentParseError(
                f'Tried to parse section in unexpected state {doc_state}')

        return end_index

    def generate_entries(self, num_entries):
        assert len(self.items) == 1, 'Should only have one template item'
        template_index, template_item = self.items[0]
        anchor = self.container['content'][template_index - 1]
        content_cell = template_item['table']['tableRows'][0]['tableCells'][0]

        updates = []
        for i in range(self.entry_shape[0]):
            updates.append(make_delete_table_row_request(template_item['startIndex'],
                                                         i))
        for _ in range(num_entries):
            updates.append(make_insert_table_request(anchor['endIndex'] - 1,
                           self.entry_shape[0], self.entry_shape[1]))

        # It's key to store this information away for the future, otherwise all
        # our future parses will be wrong
        self.num_items = num_entries
        self.generated_entries = True
        return updates

    def _make_get_table_start(self, r, c):
        def get_table_start(table):
            return (table['table']
                         ['tableRows'][r]
                         ['tableCells'][c]
                         ['content'][0]['startIndex'])
        return get_table_start


    def generate_style_updates(self):
        if not self.generated_entries:
            raise DocumentParseError(
                f'{self.name} tried to generate style updates before '
                 'generating entries!')

        style_updates = []
        for (r, c), template in self.templates.items():
            get_table_start = self._make_get_table_start(r, c)
            style_updates.extend([
                make_table_cell_style_request(template.cell_style,
                                              table['startIndex'],
                                              r,c)
                for _, table in self.items
            ])
            style_updates.extend([
                make_paragraph_style_request(style, get_table_start(table))
                for style in template.paragraph_styles
                for _, table in self.items
            ])
            style_updates.extend([
                make_text_style_request(style, get_table_start(table))
                for style in template.text_styles
                for _, table in self.items
            ])

        return style_updates

    def generate_insert_text_updates(self):
        if not self.generated_entries:
            raise DocumentParseError(
                f'{self.name} tried to generate insert text updates before '
                 'generating entries!')

        insert_updates = []
        for (r, c), template in self.templates.items():
            get_table_start = self._make_get_table_start(r, c)
            insert_updates.extend([
                make_insert_text_request(template.text.format(n=n),
                                         get_table_start(table))
                for n, (_, table) in enumerate(self.items)
            ])
        return insert_updates

    def _parse_structure(self, container, start_index):
        # This is the 'main grid' cell that holds this section
        self.container = container

        tables = get_tables(container['content'])

        # Note: num_items doesn't count the header item, so we add one
        end_index = start_index + self.num_items + 1

        # Section header item, which is always a table
        # Stored as (index, table)
        self.header = tables[start_index]

        # These are our section's elements in the container.
        # Note that 'elements' of a section are always Tables, which are
        # always at least separated by at least one Paragraph element, so
        # these indices are not contigous
        #
        # Learn more about Doc structure:
        # https://developers.google.com/docs/api/concepts/structure
        #
        # Each item here is an (index, table) pair
        self.items = tables[start_index + 1 : end_index]

        # Return the following index for the next section in this container
        return end_index

    def _parse_template_cell_content(self, table, row, col):
        content_cell = table['table']['tableRows'][row]['tableCells'][col]
        template = Template()

        template.cell_style = content_cell['tableCellStyle']

        offset = 0
        for paragraph in content_cell['content']:
            assert 'paragraph' in paragraph, 'All elements of template cells should be Paragraphs'
            paragraph_style = {
                'start': offset,
                'style': paragraph['paragraph']['paragraphStyle']
            }
            for element in paragraph['paragraph']['elements']:
                assert 'textRun' in element, 'All elements of paragraphs should be TextRuns'
                text_style = {
                    'start': offset,
                    'style': element['textRun']['textStyle']
                }

                content = element['textRun']['content']

                # We are going to add 3 characters (a 3 digit index) to every
                # template item we substitute in for, so adjust for that
                #
                # We start with the given length from the doc, rather than just
                # the length of the content, because I'm not sure if GDocs and
                # Python count larger unicode chars in the same way
                length = element['endIndex'] - element['startIndex']
                length += content.count(']]') * 3

                offset += length
                text_style['end'] = offset
                text_style['content'] = content

                # Update all our return values
                #
                # Template text has a number formatter added to it so the index
                # can be injected appropriately later
                template.text += content.replace(']]', '{n:03d}]]')
                template.text_styles.append(text_style)

            paragraph_style['end'] = offset

            template.paragraph_styles.append(paragraph_style)

        return template

    def _parse_template_content(self):
        """Fills out the template object for this section"""

        assert len(self.items) == 1, f'{self.name}, should only have one template item'
        template_table = self.items[0][1]
        for r in range(self.entry_shape[0]):
            for c in range(self.entry_shape[1]):
                template = self._parse_template_cell_content(template_table, r,
                                                             c)
                self.templates[(r, c)] = template

def update_contact_info(resume):
    to_update = {}
    to_update['contact_name'] = ('{} {}'.format(
        resume['contact']['first_name'],
        resume['contact']['last_name']))

    to_update['phone'] = resume['contact']['phone_primary']
    to_update['email'] = resume['contact']['email_primary']['email']
    to_update['city'] = 'Baltimore'
    to_update['state'] = 'MD'
    to_update['primary_function'] = ''

    return list(map(make_replace_request, to_update.items()))

def build_layout():
    # This code should be updated when the Google Doc Template is updated
    #
    # The indicies in which the section are added are the (row, column) of
    # the top level grid in which this section resides
    layout = Layout()
    for section in SECTIONS:
        layout.add_section(section['row'], section['col'],
                           Section(section['name'], shape=section['shape']))
    return layout

### NEEDS TO CHANGE
def generate_entries_from_resume(resume, layout):
    relevant_exp = resume['relevant_exp_dump']
    other_exp = resume['other_exp_dump']
    relevant_edu = resume['relevant_edu_dump']
    other_edu = resume['other_edu_dump']
    relevant_achieve = resume['relevant_achieve_dump']
    other_achieve = resume['other_achieve_dump']
    relevant_skills = resume['relevant_skills_dump']
    other_skills = resume['other_skills_dump']

    num_entries = {
        'Relevant Experience': len(relevant_exp),
        'Skills and Abilities': len(relevant_skills),
        'Achievements': len(relevant_achieve),
        'Relevant Education': len(relevant_edu),
        'Additional Experience': len(other_exp),
        'Additional Education': len(other_edu),
        'Other Achievements': len(other_achieve),
        'Additional Skills': len(other_skills),
        'Languages': 2,
    }
    return layout.generate_entries(num_entries)

def generate_content_updates(resume):
    updates = []
    updates.extend(generate_experience_updates(resume))

def generate_tag_updates(resume):
    relevant_skills = resume['relevant_skills_dump']
    other_skills = resume['other_skills_dump']

    updates = []
    to_update = {}
    for i, tag in enumerate(tags):
        n = '{:03d}'.format(i)
        to_update = {
            f'sa_tag{n}': tag['name'],
            f'sa_score{n}': tag['score']
        }
        updates.extend(
            [make_replace_request(update) for update in to_update.items()]
        )

    return updates

def generate_experience_updates(resume):
    relevant_exp = resume['relevant_exp_dump']
    other_exp = resume['other_exp_dump']
    relevant_edu = resume['relevant_edu_dump']
    other_edu = resume['other_edu_dump']
    relevant_achieve = resume['relevant_achieve_dump']
    other_achieve = resume['other_achieve_dump']

    updates = []

    #creates updates for relevant_exp
    for i, exp in enumerate(relevant_exp):
        n = '{:03d}'.format(i)
        if exp['end_year'] == 0 or exp['end_month'] == 'none':
            exp['date'] = f'{exp["start_month"]} {exp["start_year"]}–Present'
        else:
            exp['date'] = (f'{exp["start_month"]} {exp["start_year"]}'
                           f'–{exp["end_month"]} {exp["end_year"]}')
        to_update = {}
        for key in ('host', 'location', 'title', 'date'):
            to_update[f'rex_{key}{n}'] = exp[key]
        to_update[f'rex_achievements{n}'] = '\n'.join(
            [x['description'] for x in exp['achievements']])
        updates.extend(
            list(map(make_replace_request, to_update.items()))
        )

    #creates updates for other_exp
    for i, exp in enumerate(other_exp):
        n = '{:03d}'.format(i)
        if exp['end_year'] == 0 or exp['end_month'] == 'none':
            exp['date'] = f'{exp["start_month"]} {exp["start_year"]}–Present'
        else:
            exp['date'] = (f'{exp["start_month"]} {exp["start_year"]}'
                           f'–{exp["end_month"]} {exp["end_year"]}')
        to_update = {}
        for key in ('host', 'location', 'title', 'date'):
            to_update[f'aex_{key}{n}'] = exp[key]
        to_update[f'aex_achievements{n}'] = '\n'.join(
            [x['description'] for x in exp['achievements']])
        updates.extend(
            list(map(make_replace_request, to_update.items()))
        )

    #creates updates for relevant_edu
    for i, experience in enumerate(relevant_edu):
        n = '{:03d}'.format(i)
        to_update = {}
        to_update[f're_date{n}'] = '{} {}'.format(
            experience['end_month'],
            experience['end_year'])
        to_update[f're_institution{n}'] = experience['host']
        to_update[f're_degree{n}'] = experience['degree']
        updates.extend(
            list(map(make_replace_request, to_update.items()))
        )

    #creates updates for other_edu
    for i, experience in enumerate(other_edu):
        n = '{:03d}'.format(i)
        to_update = {}
        to_update[f'ae_date{n}'] = '{} {}'.format(
            experience['end_month'],
            experience['end_year'])
        to_update[f'ae_institution{n}'] = experience['host']
        to_update[f'ae_degree{n}'] = experience['degree']
        updates.extend(
            list(map(make_replace_request, to_update.items()))
        )

    #creates updates for relevant_achievements
    for i, experience in enumerate(relevant_achieve):
        n = '{:03d}'.format(i)
        to_update = {}
        to_update[f'a_date{n}'] = '{} {}'.format(
            experience['start_month'],
            experience['start_year'])
        to_update[f'a_host{n}'] = experience['host']
        to_update[f'a_description{n}'] = experience['description']
        updates.extend(
            [make_replace_request(item) for item in to_update.items()]
        )

    #creates updates for other_achieve
    for i, experience in enumerate(other_achieve):
        n = '{:03d}'.format(i)
        to_update = {}
        to_update[f'oa_date{n}'] = '{} {}'.format(
            experience['start_month'],
            experience['start_year'])
        to_update[f'oa_host{n}'] = experience['host']
        to_update[f'oa_description{n}'] = experience['description']
        updates.extend(
            [make_replace_request(item) for item in to_update.items()]
        )

    return updates


def edit_doc(gdocs, doc_id, data):
    resume = data

    layout = build_layout()

    def do_update(requests):
        requests = order_updates(requests)
        #pprint(requests)
        return gdocs.documents().batchUpdate(
            documentId=doc_id, body={'requests': requests}).execute()

    # UPDATE_CONTACT_INFO
    updates = update_contact_info(resume)
    do_update(updates)

    # PARSE_TEMPLATE
    document = gdocs.documents().get(documentId=doc_id).execute()
    layout.parse(document, DocState.PARSE_TEMPLATE)
    do_update(generate_entries_from_resume(resume, layout))

    # INSERT_TEMPLATE_TEXT
    document = gdocs.documents().get(documentId=doc_id).execute()
    layout.parse(document, DocState.INSERT_TEMPLATE_TEXT)
    do_update(layout.generate_insert_text_updates())

    # STYLE_TEMPLATE_ENTRIES
    document = gdocs.documents().get(documentId=doc_id).execute()
    layout.parse(document, DocState.STYLE_TEMPLATE_ENTRIES)
    do_update(layout.generate_style_updates())

    # INSERT_CONTENT
    do_update(generate_experience_updates(resume))
    #do_update(generate_tag_updates(resume))


def generate(data):
    (gdrive, gdocs) = init_services()

    # Retrieve the documents contents from the Docs service.
    response = gdrive.files().copy(fileId=DOCUMENT_ID,
                                   body={'name': data['name']}).execute()
    doc_id = response['id']
    gdrive.permissions().create(fileId=doc_id, body={
        'role': 'writer',
        'type': 'anyone',
    }).execute()
    gdrive.revisions().update(
        fileId=doc_id,
        revisionId=1,
        body={
            'published': True,
            'publishAuto': True,
            'publishedOutsideDomain': True,
        }
    ).execute()

    # Update the new copy of the template
    edit_doc(gdocs, doc_id, data)
    print(doc_id)
    return doc_id 
