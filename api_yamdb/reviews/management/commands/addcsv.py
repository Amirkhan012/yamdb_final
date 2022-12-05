""" Спринт 10. Проект YaMDb
Авторы:
        Амирхан Понежев
        Вадим Стрига
        Андрес Парра
Студенты факультета Бэкенд. Когорта 14+

Основная функция addcsv.py:
Импортирует данные из файлов CSV.
Для этого проекта, вы должны импортировать файлы в следующем порядке:
        1 - users.csv
        2 - category.csv
        3 - genre.csv
        4 - titles.csv
        5 - genre_title.csv
        6 - review.csv
        7 - comments.csv
Порядок важен, чтобы не было конфликтов при импорте данных.

"""
import csv

from django.core.management.base import BaseCommand, CommandError

from reviews.models import Category, Comment, Genre, Review, Title, User

CSV = {
    'users.csv': User,
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': Title,
    'review.csv': Review,
    'comments.csv': Comment,
}


class Command(BaseCommand):
    help = (
        'Import MODEL.csv into `MODEL` database.'
        'Example: python manage.py addcsv'
    )

    def handle(self, *args, **options):
        for file, model in CSV.items():
            with open('static/data/' + file, 'r', encoding="utf8") as csvFile:
                reader = csv.DictReader(csvFile, delimiter=',')
                for data in reader:
                    try:
                        model.objects.get_or_create(**data)
                    except TypeError:
                        instance = model.objects.get(id=data['id'])
                        instance.genre.add(data['genre'])
                    except Exception as e:
                        raise CommandError(e)
