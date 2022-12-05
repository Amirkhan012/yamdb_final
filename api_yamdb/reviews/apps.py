""" Спринт 10. Проект YaMDb
Авторы:
        Амирхан Понежев
        Вадим Стрига
        Андрес Парра
Студенты факультета Бэкенд. Когорта 14+

Основная функция apps.py:
Запустите приложение reviews.
"""
from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """Этот класс служит для объявления приложения в проекте."""
    name = 'reviews'
