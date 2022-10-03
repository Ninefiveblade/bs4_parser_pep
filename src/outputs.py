import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT, ARGUMENT_PRETTY, ARGUMENT_FILE

FILE_OUTPUT_MESSAGE = "Файл с результатами был сохранён: {}"


def default_output(results, cli_args):
    """Если нет аргументов выводим
    в терминал обычнчм образом."""
    if results is not None:
        for row in results:
            print(*row)


def pretty_output(results, cli_args):
    """Настраиваем параметры вывода таблицы
    в терминал."""
    if results is not None:
        table = PrettyTable()
        table.field_names = results[0]
        table.align = "l"
        table.add_rows(results[1:])
        print(table)


def file_output(results, cli_args):
    """Настраиваем директории сохранения
    csv файла."""
    if results is not None:
        results_dir = BASE_DIR / "results"
        results_dir.mkdir(exist_ok=True)
        parser_mode = cli_args.mode
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f"{parser_mode}_{now_formatted}.csv"
        file_path = results_dir / file_name
        with open(file_path, "w", encoding="utf-8") as file:
            writer = csv.writer(file, csv.unix_dialect)
            writer.writerows(results)
        logging.info(FILE_OUTPUT_MESSAGE.format(file_path))


CHOICE = {
    ARGUMENT_PRETTY: pretty_output,
    ARGUMENT_FILE: file_output,
    None: default_output
}


def control_output(results, cli_args):
    """Проверка аргумента коммандной строки
    если pretty - выводим таблицу,
    если файл, сохраняем файл."""
    CHOICE[cli_args.output](results, cli_args)
