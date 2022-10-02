from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException

MESSAGE = "Возникла ошибка при загрузке страницы {}"
TAG_MESSAGE = "Не найден тег {} {}"


def get_response(session, url):
    """Описываем функцию-перехват
    ошибок в get запросах."""

    try:
        response = session.get(url)
        response.encoding = "utf-8"
        return response
    except RequestException:
        raise RequestException(
            MESSAGE.format(url)
        )


def find_tag(soup, tag, attrs=None):
    """Описываем функцию-перехват
    для несущесвующих attrs параметров
    метода find bs4."""

    searched_tag = soup.find(tag, attrs if attrs is not None else {})
    if searched_tag is None:
        raise ParserFindTagException(TAG_MESSAGE.format(tag, attrs))
    return searched_tag


def get_soup_object(response):
    return BeautifulSoup(response.text, features="lxml")
