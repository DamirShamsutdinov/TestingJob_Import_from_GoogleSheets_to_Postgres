## Выгрузка данных из Google Sheets API в PostgreSQL

### Стек технологий
![python version](https://img.shields.io/badge/Python-3.7-yellowgreen) 
![psycopg2 version](https://img.shields.io/badge/psycopg2-2.9-yellowgreen) 
![google--api--python--client version](https://img.shields.io/badge/google--api--python--client-2.55-yellowgreen) 
![urllib3 version](https://img.shields.io/badge/urllib3-1.26-yellowgreen) 
![crontab](https://img.shields.io/badge/crontab-grey) 


### Выполняемые функции скрипта

1. Получил данные с документа при помощи Google API, сделанного в Google Sheets.

2. Данные добавляются в БД, в том же виде, что и в файле –источнике, с добавлением колонки «стоимость в руб.»

   a. Создал DB, СУБД на основе PostgreSQL.

   b. Данные для перевода $ в рубли по курсу [ЦБ РФ](https://www.cbr.ru/development/SXML/).

3. Скрипт работает постоянно для обеспечения обновления данных в онлайн режиме (Данные Google Sheets могут изменяться. Как и изменяется курс ЦБ).
<br>
Также можно чз worker на Heroky запустить (читерство), а можно чз Celery попробовать (не было времени).

### Инструкция по запуску скрипта на постоянной основе в Linux
Команды выполняются в терминале. 

Сначала клонируем репозиторий в необходимое место:
```
git clone https://github.com/DamirShamsutdinov/TestingJob_Import_from_GoogleSheets_to_Postgres.git
```

Необходимо войти в директорию проекта:
```
cd TestingJob_Import_from_GoogleSheets_to_Postgres
```

С помощью инструмента **crontab** настраиваем автозапуск скрипта *main*
```
crontab -e
```

Открывается окно VIM, где мы вводим:
```
* * * * * bash run.sh
```
Далее сохраняем и выходим ":wq"

### Итог
Таким образом скрипт будет выполняться каждую минуту и записи в БД будут обновляться

### Дополнение
Если API чувствительно к запросам, 
то необходимо прежде распарсеные данные сохранять в отдельный файл (с помощью with).
НО это не тема этого задания.


