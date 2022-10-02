import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from configs import ARGUMENT_CHOICES, configure_logging
from constants import BASE_DIR, DATETIME_FORMAT

MESSAGE = 'Файл с результатами был сохранён: {}'


def control_output(results, cli_args):
    """Проверка аргумента коммандной строки
    если pretty - выводим таблицу,
    если файл, сохраняем файл."""
    CHOICE = {
        ARGUMENT_CHOICES[0]: pretty_output,
        ARGUMENT_CHOICES[1]: file_output,
        None: default_output
    }

    CHOICE[cli_args.output](results, cli_args)


def default_output(results, cli_args):
    """Если нет аргументов выводим
    в терминал обычнчм образом."""

    for row in results:
        print(*row)


def pretty_output(results, cli_args):
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
    with open(file_path, 'w', encoding='utf-8') as file:
        writer = csv.writer(file, csv.unix_dialect)
        writer.writerows(results)
    logging.info(MESSAGE.format(file_path))
