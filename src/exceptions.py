class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""


class InfoNotFound(Exception):
    """Вызывается, когда нет информации в искомых тегах."""


class EmtyResults(Exception):
    """Вызывается, когда нет результатов."""


class ArgumentParserError(Exception):
    """Выводим ошибку, если не переданы аргументы."""
