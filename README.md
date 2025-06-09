# TG_fastAPI

Телеграм бот для просмотра постов с админкой на FastAPI

---

# Технологии⚙️
* python 3.11
* FastAPI
* Tortoise ORM + Aerich (миграции)
* PostgreSQL
* Docker + Docker Compose
* PythonTelegramBot
* JWT (аутентификация)
---
# Установка и запуск🚀
1) Клонировать репозиторий любым удобным способом
2) Установить docker и docker-compose
3) Собрать контейнер командой:
    ```commandline
    docker-compose up --build
    ```
4) Дождаться миграций (они запускаются автоматически через aerich)
5) FastAPI будет доступен по адресу http://localhost:8000
6) Телеграм-бот запускается параллельно и подключается к API
    доступен тут: https://t.me/TgFastApiTestBot
---
# Структура проекта🌳

## API
Проект адмники на FastAPI

- [app](app)
- - [auth](app/auth) - эндпоинты регистрации и авторизации
- - [posts](app/posts) - эндпоинты постов и их логика
- - [schemas](app/schemas) - pydentic schemas для постов и эндпоинтов авторизации
- - [security](app/security) - логика работы с JWT
- - [main](app/main.py) - точка входа проекта
- - [logger_config](app/logger_config.py) - конфиг для логера
---

## Bot
Проект телеграм-бота

- [bot](bot)
- - [api_client](bot/api_client.py) - функции для взаимодействия с API
- - [keyboards](bot/keyboards.py) - создание клавиатур
- - [posts](bot/posts.py) - обработка команд и callback связанных с постами
- - [utils](bot/utils.py) - вспомогательные утилиты
- - [main](bot/main.py) - точка входа бота
- - [logger_config](bot/logger_config.py) - конфиг для логера

---
## База данных
Работа с PostgreSQL, миграции

- [db](db) - Модели БД
- [configs](configs) - конфигурация подключения Tortoise ORM + Aerich к PostgreSQL
- [migrations](migrations) - мигарции
---

## Инфраструктура
Настройка и развертка контейнера и `images`, настройки `Aerich`, зависимости `python`
- [docker-compose](docker-compose.yml)
- [Dockerfile](Dockerfile)
- [poetry.lock](poetry.lock)
- [pyproject.toml](pyproject.toml)
- [requirements.txt](requirements.txt)
- [.env](.env)
-
---
# API

---

# Telegram Bot

---
