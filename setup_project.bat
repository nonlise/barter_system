@echo off
:: 1. Настройка виртуального окружения
python -m venv venv
call venv\Scripts\activate

:: 2. Установка пакетов
pip install --upgrade pip
pip install asgiref certifi charset-normalizer coreschema Django django-filter djangorestframework drf-yasg idna inflection itypes Jinja2 Markdown MarkupSafe packaging pytz PyYAML requests sqlparse typing_extensions tzdata uritemplate urllib3

:: 3. Применение миграций
python manage.py makemigrations
python manage.py migrate

echo Project setup completed successfully
pause