class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""


class InfoNotFound(Exception):
    """Вызывается, когда нет информации в искомых тегах."""


class EmtyResults(Exception):
    """Вызывается, когда нет результатов."""


class RequestConnectionError(Exception):
    """Выводим ошибку, если произошла ошибка при подключении."""
