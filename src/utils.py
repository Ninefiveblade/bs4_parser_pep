from bs4 import BeautifulSoup
from requests import RequestException
from requests.exceptions import MissingSchema

from exceptions import (
    ParserFindTagException, RequestConnectionError
)
from constants import BASE_DIR


RESPINSE_MESSAGE = "Возникла ошибка при загрузке страницы {}"
TAG_MESSAGE = "Не найден тег {} {}"


def get_response(session, url):
    """Описываем функцию, делающую
    get запрос и возвращающую ответ."""

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
    """Выполняет get_response и возвращает объект супа."""

    return BeautifulSoup(get_response(session, url).text, features="lxml")


def find_tag(soup, tag, attrs=None):
    """Описываем функцию-перехват
    для пустых тегов bs4."""

    searched_tag = soup.find(tag, attrs if attrs is not None else {})
    if searched_tag is None:
        raise ParserFindTagException(TAG_MESSAGE.format(tag, attrs))
    return searched_tag


def log_file():
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    return log_dir / "parser.log"


def downloads_dir():
    """Изначально было так, но пайтест потребовал это
    в main.py"""

    downloads_dir = BASE_DIR / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    return downloads_dir
