import threading
import time

import schedule

from GH_api import parser_GH
from push_postgres import push_postgres

"""Решил настроить автозапуск функций чз schedule"""


# В моем понимании кажд.10сек(по моим параметрам) должны запускаться функции парсинга
# И когда я поменял данные в Google Sheets API то они также должны меняться и в БД
# Нажимаю запрос - проходит успешно, но данные в БД не меняются
# Так и не решил проблему
# ЕСЛИ дадите код-ревью по возможности реализации - буду премного благодарен!


def run_push_postgres(push_postgres_func):
    parser_GH_thread = threading.Thread(target=push_postgres_func)
    parser_GH_thread.start()


schedule.every(10).seconds.do(run_push_postgres, push_postgres(parser_GH()))
while 1:
    schedule.run_pending()
    time.sleep(1)

# Можно конечно еще чз Celery
# Но в основной документации Celery настройки прописаны к проекту Джанго
# А это опять же время (при этом не факт что заработает)
