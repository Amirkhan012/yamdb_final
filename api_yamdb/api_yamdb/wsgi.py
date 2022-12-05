""" Спринт 10. Проект YaMDb
Авторы:
        Амирхан Понежев
        Вадим Стрига
        Андрес Парра
Студенты факультета Бэкенд. Когорта 14+

Основная функция wsgi.py:
включите настройки, описанные в файле settings.py.

"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')

application = get_wsgi_application()
