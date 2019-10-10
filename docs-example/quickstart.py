from __future__ import print_function
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

def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
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

    # Retrieve the documents contents from the Docs service.
    response = gdrive.files().copy(fileId=DOCUMENT_ID, body={'name': 'Automatic Test File'}).execute()
    doc_id = response['id']
    print(f'https://docs.google.com/document/d/{doc_id}/edit')
    #document = gdocs.documents().get(documentId=doc_id).execute()
    edit_doc(gdocs, doc_id)

def make_replace_request(item):
    (key, value) = item
    return {
        'replaceAllText': {
            'containsText': {
                'text': r'{{' + key + '}}',
                'matchCase': 'true'
            },
            'replaceText': value
        }
    }

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

    requests = list(map(make_replace_request, to_update.items()))
    result = gdocs.documents().batchUpdate(
        documentId=doc_id, body={'requests': requests}).execute()


def load_info(filename):
    with open(filename, 'r') as f:
        info = json.load(f)
        return info



    #print('The title of the document is: {}'.format(document.get('title')))
    #print(json.dumps(document))


if __name__ == '__main__':
    main()
