from __future__ import print_function
import sys
import pickle
import os.path
import json
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


def parse_template_cell(cell):
    template_text = ''
    cell_style = cell['tableCellStyle']
    paragraph_styles = []
    text_styles = []

    offset = 0
    for paragraph in cell['content']:
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
            template_text += content.replace(']]', '{n:03d}]]')
            text_styles.append(text_style)

        paragraph_style['end'] = offset

        paragraph_styles.append(paragraph_style)

    return (
        template_text,
        cell_style,
        paragraph_styles,
        text_styles,
    )

def parse_template_doc(document):
    # This will start out _super_ brittle and linked to the template, but we'll
    # see if it ever needs to become more robust
    mainGrid = document['body']['content'][2]
    assert 'table' in mainGrid
    assert mainGrid['table']['rows'] == 3
    assert mainGrid['table']['columns'] == 2

    relevantExperience = mainGrid['table']['tableRows'][1]['tableCells'][0]
    assert 'table' in relevantExperience['content'][3]
    newTableAnchor = relevantExperience['content'][2]
    table = relevantExperience['content'][3]
    cell = table['table']['tableRows'][0]['tableCells'][0]
    return ([
        make_delete_table_row_request(table['startIndex'], 0),
        make_insert_table_request(newTableAnchor['startIndex']),
        make_insert_table_request(newTableAnchor['startIndex']),
        make_insert_table_request(newTableAnchor['startIndex']),
    ], parse_template_cell(cell))
    
TEMPLATE_TEXT = """[[rex_host{n:03d}]] \u2014 [[rex_location_city{n:03d}]], [[rex_location_state{n:03d}]]
[[rex_title{n:03d}]]
[[rex_date_start{n:03d}]]\u2013[[rex_date_end{n:03d}]]
[[rex_achievements{n:03d}]]"""

def add_templates(document, parse_info):
    (
        template_text,
        cell_style,
        paragraph_styles,
        text_styles,
    ) = parse_info

    # This will start out _super_ brittle and linked to the template, but we'll
    # see if it ever needs to become more robust
    mainGrid = document['body']['content'][2]
    assert 'table' in mainGrid
    assert mainGrid['table']['rows'] == 3
    assert mainGrid['table']['columns'] == 2

    relevantExperience = mainGrid['table']['tableRows'][1]['tableCells'][0]
    tables = []
    for element in relevantExperience['content']:
        if 'table' in element:
            tables.append(element)

    def get_table_start(table):
        return table['table']['tableRows'][0]['tableCells'][0]['content'][0]['startIndex']

    # strip off header table, and reverse (for efficiency)
    # see https://developers.google.com/docs/api/how-tos/best-practices#edit_backwards_for_efficiency
    tables = list(reversed(list(enumerate(tables[1:]))))
    style_requests = [
        make_table_cell_style_request(cell_style, 
                                      table['startIndex'],
                                      0,0)
        for _, table in tables
    ] + [
        make_paragraph_style_request(style, get_table_start(table))
        for style in paragraph_styles
        for _, table in tables
    ] + [
        make_text_style_request(style, get_table_start(table))
        for style in text_styles
        for _, table in tables
    ]

    insert_text_requests = [
        make_insert_text_request(template_text.format(n=n), 
                                 get_table_start(table))
        for n, table in tables
    ]

    return (insert_text_requests, style_requests)

def edit_doc(gdocs, doc_id):
    info = load_info('./david.json')
    to_update = {}
    to_update['contact_name'] = ('{} {}'.format(
        info['contacts']['data']['first_name'],
        info['contacts']['data']['last_name']))

    to_update['phone'] = info['contacts']['data']['phone_primary']
    to_update['email'] = info['contacts']['data']['email_primary']['email']
    to_update['city'] = 'Tuscaloosa'
    to_update['state'] = 'AL'
    to_update['primary_function'] = 'Software Engineer'

    def do_update(requests):
        return gdocs.documents().batchUpdate(
            documentId=doc_id, body={'requests': requests}).execute()

    requests = list(map(make_replace_request, to_update.items()))
    do_update(requests)

    document = gdocs.documents().get(documentId=doc_id).execute()
    requests, parse_info = parse_template_doc(document)
    #print(json.dumps(parse_info))
    #return
    do_update(requests)

    document = gdocs.documents().get(documentId=doc_id).execute()
    (insert_requests, style_requests) = add_templates(document, parse_info)
    do_update(insert_requests)

    document = gdocs.documents().get(documentId=doc_id).execute()
    #print(json.dumps(document))
    (insert_requests, style_requests) = add_templates(document, parse_info)
    do_update(style_requests)


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
    #with open('empty_doc.json', 'r') as f:
    #    pprint(parse_template_doc(json.load(f)))

    #with open('parse_info.json', 'r') as f:
    #    parse_info = json.load(f)

    #with open('test.json', 'r') as f:
    #    pprint(add_templates(json.load(f), parse_info))

    #dump_document('1eNOSyhxsKjQZBMBgMgnEtgcpdTrj95kCrUBGxr-84zg')
    #dump_document('1RExcI9pWu6JTGqHDtXzfF0hnOj0U4KQtKf4qpFzXfwE')

    main()
