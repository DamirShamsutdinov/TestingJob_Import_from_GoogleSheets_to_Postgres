## Выгрузка данных из Google Sheets API в PostgreSQL

### Стек технологий
![python version](https://img.shields.io/badge/Python-3.7-yellowgreen) 
![psycopg2 version](https://img.shields.io/badge/psycopg2-2.9-yellowgreen) 
![google--api--python--client version](https://img.shields.io/badge/google--api--python--client-2.55-yellowgreen) 
![urllib3 version](https://img.shields.io/badge/urllib3-1.26-yellowgreen) 
![schedule version](https://img.shields.io/badge/schedule-1.1-yellowgreen) 


**Исполнено**

1. Получил данные с документа при помощи Google API, сделанного в Google Sheets.

2. Данные добавляются в БД, в том же виде, что и в файле –источнике, с добавлением колонки «стоимость в руб.»

   a. Создал DB, СУБД на основе PostgreSQL.

   b. Данные для перевода $ в рубли по курсу [ЦБ РФ](https://www.cbr.ru/development/SXML/).


**Не выполнил**

3. Скрипт работает постоянно для обеспечения обновления данных в онлайн режиме (необходимо учитывать, что строки в Google Sheets таблицу могут удаляться, добавляться и изменяться).
<br>
**К сожалению так и не решил задачу с автозапуском скрипта с помощью *schedule*** 
<br>
Можно чз worker на Heroky запустить (читерство), а можно чз Celery попробовать (не было времени).

### Инструкция по запуску
Клонировать репозиторий через терминал bash:

```
git clone https://github.com/DamirShamsutdinov/Import_from_GoogleSheets_to_Postgres.git
```

Cоздать и активировать виртуальное окружение:

```
WIN: python -m venv venv
MAC: python3 -m venv venv
```

```
WIN: source venv/scripts/activate
MAC: source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
WIN: python -m pip install --upgrade pip
MAC: python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить скрипт:

```
WIN: python main.py
MAC: python3 main.py
```