from __future__ import print_function
import sys
import pickle
import os.path
import json
from enum import Enum
from collections import defaultdict 
from pprint import pprint

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive'
]

# The ID of a sample document.
FILLED_DOCUMENT_ID = '1R80Bdc5eGdAIQJ3UULX_GRLkSAOV49H8qfZb5PMs1gs'
TEST_DOCUMENT_ID = '1RExcI9pWu6JTGqHDtXzfF0hnOj0U4KQtKf4qpFzXfwE'
DOCUMENT_ID = TEST_DOCUMENT_ID

def init_services():
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

def make_insert_table_request(location):
    return {
        'insertTable': {
            'rows': 1,
            'columns': 1,
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

def get_tables(elements):
    tables = []
    for elem_index, element in enumerate(elements):
        if 'table' in element:
            tables.append((elem_index, element))
    return tables

def generate_experience_updates(experiences):
    experiences = resume['experiences']['data']

    updates = []
    for i, experience in enumerate(experiences):
        n = '{:03d}'.format(i)
        to_update = {}
        for key in ('host', 'location_city', 'location_state', 'title'):
            to_update[f'rex_{key}{n}'] = experience[key]
        for key in ('start', 'end'):
            to_update[f'rex_date_{key}{n}'] = '{} {}'.format(
                experience[key + '_month'],
                experience[key + '_year'])
        to_update[f'rex_achievements{n}'] = '\n'.join(
            map(lambda x: x['description'], experience['achievements']))
        updates.extend(
            list(map(make_replace_request, to_update.items()))
        )

    return updates

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

    def generate_insert_text_updates(self, num_entries):
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
    def __init__(self, name):
        self.name = name 
        # Every section starts with a template entry
        self.num_items = 1
        self.container = None
        self.template = None

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

        updates = [
            make_delete_table_row_request(template_item['startIndex'], 0),
        ]
        for _ in range(num_entries):
            updates.append(make_insert_table_request(anchor['endIndex'] - 1))

        # It's key to store this information away for the future, otherwise all
        # our future parses will be wrong
        self.num_items = num_entries
        self.generated_entries = True
        return updates

    def generate_style_updates(self):
        if not self.generated_entries:
            raise DocumentParseError(
                f'{self.name} tried to generate style updates before generating entries!')

        style_updates = [
            make_table_cell_style_request(self.template.cell_style, 
                                          table['startIndex'],
                                          0,0)
            for _, table in self.items
        ]
        style_updates.extend([
            make_paragraph_style_request(style, get_table_start(table))
            for style in self.template.paragraph_styles
            for _, table in self.items
        ])
        style_updates.extend([
            make_text_style_request(style, get_table_start(table))
            for style in self.template.text_styles
            for _, table in self.items
        ])

        return style_updates

    def generate_insert_text_updates(self):
        if not self.generated_entries:
            raise DocumentParseError(
                f'{self.name} tried to generate insert text updates before generating entries!')

        return [
            make_insert_text_request(self.template.text.format(n=n), 
                                     get_table_start(table))
            for n, (_, table) in enumerate(self.items)
        ]


    def _parse_structure(self, container, start_index):
        # This is the 'main grid' cell that holds this section
        self.container = container

        pprint(container)
        tables = get_tables(container['content'])
        pprint(tables)

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
        pprint(self.items)

        # Return the following index for the next section in this container
        return end_index

    def _parse_template_content(self):
        """Fills out the template object for this section"""

        assert len(self.items) == 1, f'{self.name}, should only have one template item'
        template_index, template_item = self.items[0]
        anchor = self.container['content'][template_index - 1]
        content_cell = template_item['table']['tableRows'][0]['tableCells'][0]

        self.template = Template()
        self.template.cell_style = content_cell['tableCellStyle']

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
                self.template.text += content.replace(']]', '{n:03d}]]')
                self.template.text_styles.append(text_style)

            paragraph_style['end'] = offset

            self.template.paragraph_styles.append(paragraph_style)

def update_contact_info(resume):
    to_update = {}
    to_update['contact_name'] = ('{} {}'.format(
        resume['contacts']['data']['first_name'],
        resume['contacts']['data']['last_name']))

    to_update['phone'] = resume['contacts']['data']['phone_primary']
    to_update['email'] = resume['contacts']['data']['email_primary']['email']
    to_update['city'] = 'Tuscaloosa'
    to_update['state'] = 'AL'
    to_update['primary_function'] = 'Software Engineer'

    return list(map(make_replace_request, to_update.items()))

def build_layout():
    # This code should be updated when the Google Doc Template is updated
    #
    # The indicies in which the section are added are the (row, column) of
    # the top level grid in which this section resides
    layout = Layout()
    layout.add_section(1, 0, Section('Relevant Experience'))
    layout.add_section(1, 1, Section('Skills and Abilities'))
    layout.add_section(1, 1, Section('Achivements'))
    layout.add_section(1, 1, Section('Relevant Education'))
    layout.add_section(2, 0, Section('Additional Experience'))
    layout.add_section(2, 1, Section('Additional Education'))
    layout.add_section(2, 1, Section('Other Achievements'))
    layout.add_section(2, 1, Section('Additional Skills'))
    layout.add_section(2, 1, Section('Languages'))

    return layout

def generate_entries_from_resume(resume, layout):
    experiences = resume['experiences']['data']
    work_experiences = filter(lambda e: e['type'] == 'Work', experiences)
    edu_experiences = filter(lambda e: e['type'] == 'Education', experiences)
    service_experiences = filter(lambda e: e['type'] == 'Service', experiences)
    accomplishments = filter(lambda e: e['type'] == 'Accomplishment', experiences)

    num_entries = {
        'Relevant Experience': len(work_experiences),
        'Skills and Abilities': 0,
        'Achievements': len(accomplishments),
        'Relevant Education': len(edu_experiences),
        'Additional Experience': 0,
        'Additional Education': 0,
        'Other Achievements': 0,
        'Additional Skills': 0,
        'Languages': 0,
    }
    layout.generate_entries(num_entries)

def generate_content_updates(resume):
    updates = []
    updates.extend(generate_experience_updates(resume))

def edit_doc(gdocs, doc_id):
    resume = load_info('./david.json')

    layout = build_layout()

    def do_update(requests):
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


def load_info(filename):
    with open(filename, 'r') as f:
        info = json.load(f)
        return info

def main():
    (gdrive, gdocs) = init_services()

    # Retrieve the documents contents from the Docs service.
    response = gdrive.files().copy(fileId=DOCUMENT_ID, body={'name': 'Automatic Test File'}).execute()
    doc_id = response['id']
    print(f'https://docs.google.com/document/d/{doc_id}/edit', file=sys.stderr)
    edit_doc(gdocs, doc_id)



if __name__ == '__main__':
    layout = build_layout()
    with open('empty_doc.json', 'r') as f:
        doc = json.load(f)
        layout.parse(doc, DocState.PARSE_TEMPLATE)

    #with open('parse_info.json', 'r') as f:
    #    parse_info = json.load(f)

    #with open('test.json', 'r') as f:
    #    pprint(add_templates(json.load(f), parse_info))

    #dump_document('1eNOSyhxsKjQZBMBgMgnEtgcpdTrj95kCrUBGxr-84zg')
    #dump_document('1RExcI9pWu6JTGqHDtXzfF0hnOj0U4KQtKf4qpFzXfwE')

    #main()