""" Спринт 10. Проект YaMDb
Авторы:
        Амирхан Понежев
        Вадим Стрига
        Андрес Парра
Студенты факультета Бэкенд. Когорта 14+

YaMDb URL Configuration

http:+ // + IP-адрес локального сервера + / +

admin/ ->   перенаправление на панель управления Django.
api/   ->   доступ к API проекта YamDb
redoc/ ->   доступ к требованиям заказчика для разработки проекта YamDb
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'api/',
        include('api.urls')
    ),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
