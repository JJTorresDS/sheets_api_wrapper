import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# docs: https://developers.google.com/sheets/api/quickstart/python
# If modifying these scopes, delete the file token.json.


# The ID and range of a sample spreadsheet.
# https://docs.google.com/spreadsheets/d/1ch1HPp64_rGpbgCud-4Ov1sB5Z-NuMQetuoDh6Z2h-c/edit#gid=0



def main(SAMPLE_SPREADSHEET_ID, CREDENTIALS, 
          SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]):
  """
    Returns a Sheets serviced object that acts as an API fro GSheets
    SAMPLE_SPREADSHEET_ID: id of the spreadsheet you want to interface with
    CREDENTIALS: path to json document containing credentials
    SCOPES: scopes of interface, defaults to "spreadsheets"

  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          CREDENTIALS, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    return sheet
      
  except HttpError as err:
    print(err)