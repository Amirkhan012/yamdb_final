""" Спринт 10. Проект YaMDb
Авторы:
        Амирхан Понежев
        Вадим Стрига
        Андрес Парра
Студенты факультета Бэкенд. Когорта 14+

Основная функция filters.py:
С помощью класса TitleFilter выполняется фильтрация
по переменным: имя, категория жанр.
"""
from django_filters import rest_framework as filters
from reviews.models import Title


class TitlesFilter(filters.FilterSet):
    """Фильтрация зависит от переменной."""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )

    class Meta:
        """Это относится к модели Title."""
        model = Title
        fields = ['name', 'year', 'genre', 'category']
