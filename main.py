import os.path
from config import host, user, password, db_name
from curs import currency_dict

from googleapiclient.discovery import build
from google.oauth2 import service_account

from psycopg2 import connect
from psycopg2.extras import execute_values

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
SAMPLE_SPREADSHEET_ID = '1g-dwgL6aJABx64hp7LWubff_VhSjVzCDnsl92yhedLU'
SAMPLE_RANGE_NAME = 'List1!A:D'


def parser_sheets(sc, s_a_f, s_s_i, s_r_n):
    '''Parser Google Sheets API'''
    credentials = service_account.Credentials.from_service_account_file(
        s_a_f, scopes=sc)
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=s_s_i,
                                range=s_r_n).execute()
    values = result.get('values', [])
    response = service.spreadsheets().values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        majorDimension='ROWS',
        range=SAMPLE_RANGE_NAME
    ).execute()
    data = response['values'][1:]
    return data


def push_postgres(values):
    '''Import values in Postgres'''
    c = connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cr = c.cursor()

    cr.execute(
        """DROP TABLE test_c;""")

    cr.execute(
        """
        create table test_c(
                transaction_id int primary key ,
                order_id int,
                amount_usd numeric,
                amount_rub numeric generated always as (amount_usd * %s) stored,
                deadlines_delivery date
        );
        """,
        [currency_dict]
    )

    execute_values(
        cr,
        """
        insert into test_c (transaction_id, order_id, amount_usd, deadlines_delivery)
           VALUES %s
                on conflict (transaction_id) do update
                        set order_id = excluded.order_id,
                        amount_usd = excluded.amount_usd,
                        deadlines_delivery = excluded.deadlines_delivery;
        """,
        values,
        template="(%s, %s, %s, to_date(%s::text, 'DD.MM.YYYY'))",
        page_size=100
    )
    c.commit()
    cr.close()
    c.close()

if __name__ == '__main__':
    push_postgres(parser_sheets(SCOPES , SERVICE_ACCOUNT_FILE, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME))
