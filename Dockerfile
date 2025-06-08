# Используем официальный образ Python с указанием точной версии
FROM python:3.13-slim

# Устанавливаем переменные окружения для оптимизации Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Создаем и переходим в рабочую директорию
WORKDIR /tg_fastapi_project

# Копируем и устанавливаем Python-зависимости
COPY ../requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь проект (исключая ненужные файлы через .dockerignore)
COPY .. .
