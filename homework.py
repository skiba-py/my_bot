import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import (ApiException, EmptyListException, JsonException,
                        ResponseException)
from settings import ENDPOINT, HEADERS, HOMEWORK_VERDICTS, RETRY_PERIOD

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# подскажите пожалуйста по исключениям и логам,
# все ли правильно логируется, может можно где-то оптимизировать код?


def check_tokens() -> bool:
    """Проверяет доступность токенов."""
    return all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))


def send_message(bot, message: str) -> None:
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logger.debug(f'Бот отправил сообщение: {message}')
    except Exception as error:
        logger.error(f'Ошибка отправки сообщения: {error}')
        raise ResponseException(f'Ошибка отправки сообщения: {error}')


def get_api_answer(timestamp: int) -> dict:
    """Делает запрос к API практикума."""
    payload = {'from_date': timestamp}
    try:
        homework_statuses = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=payload
        )
    except Exception as error:
        raise ApiException(f'Ошибка ответа API: {error}')
    if homework_statuses.status_code != HTTPStatus.OK:
        raise ResponseException(
            f'Ошибка статуса API: {homework_statuses.status_code}'
        )
    try:
        return homework_statuses.json()
    except Exception as error:
        raise JsonException(f'Ошибка декодирования {error}')


def check_response(response: dict) -> list:
    """Проверяет ответ API."""
    if not isinstance(response, dict):
        raise TypeError('Несоответствие типов в ответе API')
    if 'current_date' not in response or 'homeworks' not in response:
        raise ApiException('Некорректный ответ API')
    if not isinstance(response.get('homeworks'), list):
        raise TypeError('Нет списка в ответе API по ключу "homeworks"')
    if not response.get('homeworks'):
        raise EmptyListException('Нет новых статусов')
    return response.get('homeworks')


def parse_status(homework: dict) -> str:
    """Извлекает из информации о домашней работе статус работы."""
    if 'homework_name' not in homework:
        raise KeyError('Ключ homework_name отсутствует')
    if 'status' not in homework:
        raise KeyError('Ключ status отсутствует')
    hw_status = homework['status']
    hw_name = homework['homework_name']
    if hw_status not in HOMEWORK_VERDICTS:
        raise KeyError(f'{hw_status} отсутствует в словаре verdicts')
    verdict = HOMEWORK_VERDICTS.get(hw_status)
    return f'Изменился статус проверки работы "{hw_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logger.critical('Отсутствуют обязательные переменные окружения!')
        sys.exit(1)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())  # - 30 * 24 * 60 * 60  # для тестирования
    previous_homework = None
    previous_error = None
    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)
            current_homework = homeworks[0]
            message = parse_status(current_homework)
            # if previous_homework is not None: - c проверкой код не работает
            if current_homework != previous_homework:
                send_message(bot, message)
            previous_homework = current_homework
        except EmptyListException:
            logger.debug('Нет новых статусов в ответе API')
        except (Exception, TypeError, ApiException,
                ResponseException, KeyError) as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            if error != previous_error:
                send_message(bot, message)
                previous_error = error
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
