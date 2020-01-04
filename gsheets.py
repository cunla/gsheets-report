from __future__ import print_function
import pickle
import os.path
from io import StringIO

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
import settings

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class NoDataFoundError(Exception):
    pass


def _build_google_client():
    """
    Build a google api client
    :return: a google api client
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
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


if __name__ == '__main__':
    file_str = read_spreadsheet_as_csv(settings.SPREADSHEET_ID, settings.SPREADSHEET_RANGE)
    print(file_str.getvalue())
