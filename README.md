# parser_yap
Парсинг PEP страниц.
Парсит страницы python, имеет возможность сохранять в файл
выводить Pretty Table

# Технологии
BeautifulSoup agrparse, request_cache, csv.

# Подготовка к запуску проекта:
Необходимо установить виртуальное окружение:
```python3.9 -m venv venv```
Установить зависимости:
```source venv/bin/activate```
```(venv) $ pip install -r requirements```

# Запуск парсера:
## whats-new
Выполните 
``` python main.py whats-new -o file ```
для сохранения в файл.
``` python main.py whats-new -o pretty ```
для вывода в терминал в виде таблицы.
## latest-versions
Выполните 
``` python main.py latest-versions -o file ```
для сохранения в файл.
``` python main.py latest-versions -o pretty ```
для вывода в терминал в виде таблицы.
## download
Выполните
``` python main.py download ```
чтобы сохранить документацию последней актуальной
версиии.
## pep
Выполните 
``` python main.py pep -o file ```
для сохранения в файл.
``` python main.py pep -o pretty ```
для вывода в терминал в виде таблицы.
# Запуск тестов:
## Из корневой директории проекта:
```(venv) $ pytest```

# Лицензия:
[LICENSE MIT](LICENSE)