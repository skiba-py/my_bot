# Проект Telegram Bot
Бот обращается к разным API с разными задачами. Написан с использованием популярных библиотек Python-telegram-bot и Aiogram.

## Содержание
- [Функционал](#функционал)
- [Технологии](#технологии)
- [Начало работы](#начало-работы)

## Функционал
- Взаимодействие с ChatGPT, бот обращается к API OpenAI, отдает запрос пользователя и возвращает ответ ChatGPT. Файл "gpt_bot.py"
- Узнает статус проверки проекта, обращается к API Практикума и возвращает статус проверки. Файл "homework.py"
- По нажатию на кнопку "new cat" отдает рандомную картинку кота. Реализовано также через обращение к API. Файл "kittybot.py"

## Технологии
- Python 3.11 ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- Python-telegram-bot
- Aiogram
- OpenAI
- Pytest

## Начало работы
### Необходимо:
1. Клонировать репозиторий:
2. Перейти в папку с проектом:
3. Установить виртуальное окружение для проекта:
```sh
python -m venv venv
``` 
4. Активировать виртуальное окружение для проекта:
```sh
# для OS Lunix и MacOS
source venv/bin/activate

# для OS Windows
source venv/Scripts/activate
```
5. Установить зависимости:
```sh
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
6. Каждый файл бота нужно запускать отдельно в зависимости от задач:
```sh
python3 <имя_файла>.py
```
