import argparse

from bs4 import BeautifulSoup
from requests import RequestException
from requests.exceptions import MissingSchema

from exceptions import (
    ParserFindTagException, ArgumentParserError, RequestConnectionError
)

RESPINSE_MESSAGE = "Возникла ошибка при загрузке страницы {}"
TAG_MESSAGE = "Не найден тег {} {}"


def get_response(session, url):
    """Заглушка для пайтест."""

    try:
        response = session.get(url)
        response.encoding = "utf-8"
        return response
    except MissingSchema as error:
        raise RequestConnectionError(
            RESPINSE_MESSAGE.format(url),
            error
        )
    except RequestException as error:
        raise RequestConnectionError(
            RESPINSE_MESSAGE.format(url),
            error
        )


def get_soup_response(session, url):
    """Описываем функцию-перехват
    ошибок в get запросах."""

    try:
        response = session.get(url)
        response.encoding = "utf-8"
        return BeautifulSoup(response.text, features="lxml")
    except MissingSchema as error:
        raise RequestConnectionError(
            RESPINSE_MESSAGE.format(url),
            error
        )
    except RequestException as error:
        raise RequestConnectionError(
            RESPINSE_MESSAGE.format(url),
            error
        )


def find_tag(soup, tag, attrs=None):
    """Описываем функцию-перехват
    для несущесвующих attrs параметров
    метода find bs4."""

    searched_tag = soup.find(tag, attrs if attrs is not None else {})
    if searched_tag is None:
        raise ParserFindTagException(TAG_MESSAGE.format(tag, attrs))
    return searched_tag


class ThrowingArgumentParser(argparse.ArgumentParser):
    """Переписываем класс, чтобы трейсить нужную ошибку."""

    def error(self, message):
        raise ArgumentParserError(
            "Не переданы или переданы неправильно основные параметры. "
            f"{message}"
        )
