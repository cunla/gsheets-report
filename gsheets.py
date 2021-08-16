from __future__ import print_function

import datetime
import pickle
import os.path
from io import StringIO
from typing import List

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
import settings

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class NoDataFoundError(Exception):
    pass


def _build_google_client():
    """
    Build a google api client
    :return: a google api client
    """
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('sheets', 'v4', credentials=creds)


def read_spreadsheet_as_csv(spreadsheet_id: str, range: str) -> StringIO:
    """
    Read a range from google spreadsheet and return it as csv
    :param spreadsheet_id spreadsheet ID
    :param range range to read
    :return csv of the range
    """
    service = _build_google_client()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range).execute()
    values = result.get('values', [])

    if not values:
        raise NoDataFoundError()
    io_str = StringIO()
    for row in values:
        io_str.write(','.join(row) + '\n')
    io_str.flush()
    return io_str


def write_new_row(spreadsheet_id: str, range: str, values: List):
    service = _build_google_client()
    body = {
        'values': [values,]
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range,
        valueInputOption='USER_ENTERED', body=body).execute()


if __name__ == '__main__':
    # file_str = read_spreadsheet_as_csv(settings.SPREADSHEET_ID, settings.SPREADSHEET_RANGE)
    # print(file_str.getvalue())
    write_new_row(settings.SPREADSHEET_ID, settings.SPREADSHEET_RANGE, ['2021-05-01', 122.2])
