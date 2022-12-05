""" Спринт 10. Проект YaMDb
Авторы:
        Амирхан Понежев
        Вадим Стрига
        Андрес Парра
Студенты факультета Бэкенд. Когорта 14+

Основная функция permissions.py:
Настройте разрешения, которые пользователь будет иметь в качестве
создателя контента, администратора или анонимного пользователя.
"""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    '''permission для Category, Genre, Title'''
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    '''permission для Review, Comment'''
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)


class IsAdmin(permissions.BasePermission):
    '''permission для Userlist'''
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)
