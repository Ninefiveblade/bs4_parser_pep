import logging

from requests import RequestException

from exceptions import ParserFindTagException


def get_response(session, url):
    """Описываем функцию-перехват
    ошибок в get запросах."""

    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        if response is not None:
            return response
        else:
            return
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    """Описываем функцию-перехват
    для несущесвующих attrs параметров
    метода find bs4."""

    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag
