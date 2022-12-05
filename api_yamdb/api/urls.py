""" Спринт 10. Проект YaMDb
Авторы:
        Амирхан Понежев
        Вадим Стрига
        Андрес Парра
Студенты факультета Бэкенд. Когорта 14+

Основная функция: определение URL-адресов проекта

"""
from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet,
                    get_jwttoken_user, registration)

version = 'v1'
app_name = 'reviews'


router = routers.DefaultRouter()
router.register(
    r'titles',
    TitleViewSet
)
router.register(
    r"users",
    UserViewSet
)
router.register(
    r'categories',
    CategoryViewSet
)
router.register(
    r'genres',
    GenreViewSet
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)


urlpatterns = [
    path(
        f'{version}/',
        include(router.urls)
    ),
    path(
        f'{version}/auth/signup/',
        registration,
        name='register'
    ),
    path(
        f'{version}/auth/token/',
        get_jwttoken_user,
        name='token'
    ),
]
