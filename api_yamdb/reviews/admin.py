""" Спринт 10. Проект YaMDb
Авторы:
        Амирхан Понежев
        Вадим Стрига
        Андрес Парра
Студенты факультета Бэкенд. Когорта 14+

Основная функция admin.py:
этот файл настраивает модели таким образом, чтобы администратор
сайта мог управлять ими из панели управления.
Эти модели:
        1 - Category
        2 - Genre
        3 - Review
        4 - Comment
        5 - User
        6 - Title
"""
from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'text', 'pub_date', 'score',)
    ordering = ('-pub_date', 'author',)
    search_fields = ('author', 'title', 'score',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'review', 'pub_date')
    ordering = ('-pub_date', 'author')
    search_fields = ('author', 'review')


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role',)
    ordering = ('username',)
    search_fields = ('username', 'email', 'role')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    ordering = ('name', 'category')
    search_fields = ('name', 'category', 'genre', 'rating')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
