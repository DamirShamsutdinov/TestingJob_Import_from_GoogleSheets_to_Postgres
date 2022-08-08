import os.path
import threading
import time

import schedule
from google.oauth2 import service_account
from googleapiclient.discovery import build


def parser_GH():
    """Parser Google Sheets API"""
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "credentials.json")
    SAMPLE_SPREADSHEET_ID = "1g-dwgL6aJABx64hp7LWubff_VhSjVzCDnsl92yhedLU"
    SAMPLE_RANGE_NAME = "List1!A:D"

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])
    response = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            majorDimension="ROWS",
            range=SAMPLE_RANGE_NAME,
        )
        .execute()
    )
    data = response["values"][1:]
    return data


# def GH_api():
#     schedule.every(5).seconds.do(parser_GH)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
