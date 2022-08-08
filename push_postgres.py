from psycopg2 import connect
from psycopg2.extras import execute_values

from config import db_name, host, password, user
from curs import currency_dict


def push_postgres(values):
    """Import values in Postgres"""
    c = connect(host=host, user=user, password=password, database=db_name)
    cr = c.cursor()

    cr.execute("""drop table if exists test_c;""")

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
        [currency_dict],
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
        page_size=100,
    )
    c.commit()
    cr.close()
    c.close()


# push_PQ = push_postgres(GH_api())
