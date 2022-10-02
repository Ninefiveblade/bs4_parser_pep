from bs4 import BeautifulSoup
from requests import RequestException
from requests.exceptions import MissingSchema

from exceptions import (
    ParserFindTagException, RequestConnectionError
)

RESPINSE_MESSAGE = "Возникла ошибка при загрузке страницы {}"
TAG_MESSAGE = "Не найден тег {} {}"


def get_response(session, url):
    """Для прохождения пайтеста."""

    try:
        response = session.get(url)
        response.encoding = "utf-8"
        return response
    except (MissingSchema, RequestException) as error:
        raise RequestConnectionError(
            RESPINSE_MESSAGE.format(url),
            error
        )


def get_soup_response(session, url):
    """Декоратор супа"""
    return BeautifulSoup(get_response(session, url).text, features="lxml")


def find_tag(soup, tag, attrs=None):
    """Описываем функцию-перехват
    для несущесвующих attrs параметров
    метода find bs4."""

    searched_tag = soup.find(tag, attrs if attrs is not None else {})
    if searched_tag is None:
        raise ParserFindTagException(TAG_MESSAGE.format(tag, attrs))
    return searched_tag
