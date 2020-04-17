'''

# Instructions

1. Access the documentation: https://developers.google.com/sheets/api/quickstart/python
2. Follow (Step 1) to create a project and download the credentials.json file
3. Move the credentials.json to the same folder as this sorce file (or update CLIENT_SECRET_FILE with the correct path)
4. Install required libs: `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

# Example of usage

import sheets

# Get the spreadsheet id from the URL
SPREADSHEET='1kU5Yua2r-PPDF8wfN_uif9fGDv-z8kFM7X-UjHZR4yM'

values = sheets.read_spreadsheet(SPREADSHEET, "Page1!D1:D2")

write_spreadsheet(SPREADSHEET, "Page1!A1:C3", [["1","2","3"],["4","5","6"],["7","8","9"]])

'''

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    return service

def read_spreadsheet(spreadsheetId, range):
    result = get_service().spreadsheets().values().get(spreadsheetId=spreadsheetId, range=range).execute()
    values = result.get('values', [])

    return values

def write_spreadsheet(spreadsheetId, range, values):
    body = {
        'values': values
    }

    result = get_service().spreadsheets().values().update(spreadsheetId=spreadsheetId, range=range, valueInputOption="RAW", body=body).execute()

    return result