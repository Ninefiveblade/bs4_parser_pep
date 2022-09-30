import datetime as dt
import csv
import logging

from prettytable import PrettyTable

from constants import DATETIME_FORMAT, BASE_DIR
from configs import configure_logging


def control_output(results, cli_args):
    """Проверка аргумента коммандной строки
    если pretty - выводим таблицу,
    если файл, сохраняем файл."""

    output = cli_args.output
    if output == 'pretty':
        pretty_output(results)
    elif output == 'file':
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results):
    """Если нет аргументов выводим
    в терминал обычнчм образом."""

    for row in results:
        print(*row)


def pretty_output(results):
    """Настраиваем параметры вывода таблицы
    в терминал."""

    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    """Настраиваем директории сохранения
    csv файла."""

    configure_logging()
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {file_path}')
