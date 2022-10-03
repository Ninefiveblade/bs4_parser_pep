import logging
import argparse
from logging.handlers import RotatingFileHandler

from constants import ARGUMENT_FILE, ARGUMENT_PRETTY
from utils import log_file

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'


def configure_argument_parser(available_modes):
    """Настройка передачи аргументов через командную
    строку."""

    parser = argparse.ArgumentParser(description='Парсер документации Python')
    parser.add_argument(
        'mode',
        choices=available_modes,
        help='Режимы работы парсера'
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша'
    )
    parser.add_argument(
        '-o',
        '--output',
        choices=(ARGUMENT_PRETTY, ARGUMENT_FILE),
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging() -> None:
    """Настройки логгирования."""

    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(
            RotatingFileHandler(
                log_file(),
                maxBytes=10 ** 6,
                backupCount=5
            ),
            logging.StreamHandler()
        )
    )
