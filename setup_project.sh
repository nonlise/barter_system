#!/bin/bash

# 1. Проверка и настройка виртуального окружения
echo "=== Setting up Python virtual environment ==="
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
# source venv/Scripts/activate  # Для Windows (раскомментируйте эту строку если используете Windows)

# 2. Установка пакетов
echo "=== Installing required packages ==="
pip install --upgrade pip
pip install asgiref certifi charset-normalizer coreschema Django django-filter djangorestframework drf-yasg idna inflection itypes Jinja2 Markdown MarkupSafe packaging pytz PyYAML requests sqlparse typing_extensions tzdata uritemplate urllib3

# 3. Применение миграций
echo "=== Applying database migrations ==="
python manage.py makemigrations
python manage.py migrate

echo "=== Project setup completed successfully ==="
echo "To start the development server, run: python manage.py runserver"