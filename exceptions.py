class ApiException(Exception):
    """Некорректный ответ API."""

    pass


class EmptyListException(Exception):
    """Статус работы не изменился."""

    pass


class ResponseException(Exception):
    """Некорректный код ответа."""

    pass


class JsonException(Exception):
    """Некоректное декодирование json."""

    pass
