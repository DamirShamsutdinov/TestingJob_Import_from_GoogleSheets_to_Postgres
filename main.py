import os.path
from pprint import pprint
from config import host, user, password, db_name
import psycopg2
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = '1g-dwgL6aJABx64hp7LWubff_VhSjVzCDnsl92yhedLU'
SAMPLE_RANGE_NAME = 'List1!A:D'

service = build('sheets', 'v4', credentials=credentials)

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=SAMPLE_RANGE_NAME).execute()

values = result.get('values', [])
# pprint(values)

# for row in values:
#     print('%s, %s, %s, %s' % (row[0], row[1], row[2], row[3]))

response = service.spreadsheets().values().get(
    spreadsheetId=SAMPLE_SPREADSHEET_ID,
    majorDimension='ROWS',
    range=SAMPLE_RANGE_NAME
).execute()

rows = response['values'][1:]
# pprint(rows)

"""Connect to exist database"""
connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)
connection.autocommit = True

# for row in rows:
#     st1 = row[0], st2 = row[1], st3 = row[2], st4 = row[3]

"""CREATE TABLE"""
# with connection.cursor() as cursor:
#     cursor.execute(
#         """CREATE TABLE test_c (
#         №   integer,
#         заказ_№ integer,
#         стоимость_$ integer,
#         стоимость_РУБ integer,
#         срок_поставки   date);"""
#     )

col1 = [row[0] for row in rows]
col2 = [row[1] for row in rows]
col3 = [row[2] for row in rows]
col4 = [row[2] * 67 for row in rows]  # курс $ через API вытащю, но пока так
col5 = [row[3] for row in rows]
print(col1)


"""INSERT data into a table"""
# with connection.cursor() as cursor:
#     cursor.execute(
#         """INSERT INTO test_c
#         (№, заказ_№, стоимость_$, стоимость_РУБ, срок_поставки)
#         VALUES (col1, col2, col3, col4, col5);"""
#     )
#
"""UPDATE data into a table"""
# with connection.cursor() as cursor:
#     cursor.execute(
#         """UPDATE test_c
#         SET № = [i for i in col1];"""
#     )

# with connection.cursor() as cursor:
#     cursor.executemany(
#         """INSERT INTO test_c VALUES(col1, col2, col3, col4, col5);"""

