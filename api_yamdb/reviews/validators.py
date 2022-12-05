""" Спринт 10. Проект YaMDb
Авторы:
        Амирхан Понежев
        Вадим Стрига
        Андрес Парра
Студенты факультета Бэкенд. Когорта 14+

Основная функция validators.py:
Опишите функцию: validator_year для проверяет текущую дату (год)
"""
from django.core.exceptions import ValidationError
from django.utils import timezone


def validator_year(value):
    """Функция, подтверждающая год публикации."""
    if value > timezone.now().year:
        raise ValidationError(
            ('Год %(value)s больше!'),
            params={
                'value': value
            },
        )
