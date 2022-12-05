""" Спринт 10. Проект YaMDb
Авторы:
        Амирхан Понежев
        Вадим Стрига
        Андрес Парра
Студенты факультета Бэкенд. Когорта 14+

Основная функция models.py:
Опишите модели проекта. Эти модели взаимодействуют с базой данных db.sqlite3.
Модели следующие:
        1 - User (AbstractUser)
        2 - Category (models.Model)
        3 - Genre (models.Model)
        4 - Title (models.Model)
        5 - Review (models.Model)
        6 - Comment (models.Model)
"""
from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    validate_slug)
from django.db import models

from .validators import validator_year


class User(AbstractUser):
    """Модель пользователей.
    Пользователь может быть администратором, модератором
    или обычным пользователем.
    Входные переменные:
    Поля email и username должны быть уникальными.
    Поля role -> Администратор, модератор или пользователь.
                 По умолчанию user.
    """
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES_USER = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Administrator'),
    ]
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        null=True
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        null=False
    )
    bio = models.TextField(
        'bio',
        null=True,
        blank=True
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=100,
        choices=ROLES_USER,
        default=USER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username'
    ]

    @property
    def is_moderator(self) -> str:
        """Если пользователь является moderator."""
        return self.role == self.MODERATOR

    @property
    def is_admin(self) -> str:
        """Если пользователь является администратором."""
        return self.role == self.ADMIN

    class Meta:
        """список сортируется по идентификатору (id)."""
        ordering = ['id']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="username_is_not_me"
            )
        ]


class Category(models.Model):
    """Категории (типы) произведений («Фильмы», «Книги», «Музыка»).
    Права доступа на создание категории: Администратор.
    Поле slug каждой категории должно быть уникальным.
    """
    name = models.CharField(
        max_length=256,
        null=False
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        null=False,
        validators=[validate_slug]
    )

    class Meta:
        """список сортируется по переменной name."""
        ordering = ('name',)

    def __str__(self) -> str:
        """Выводится название категории."""
        return self.name


class Genre(models.Model):
    """Жанры произведений.
    Права доступа на добавление жанра: Администратор.
    Поле slug каждой категории должно быть уникальным.
    """
    name = models.CharField(
        max_length=256,
        null=False
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        null=False,
        validators=[validate_slug]
    )

    class Meta:
        """список сортируется по переменной name."""
        ordering = ('name',)

    def __str__(self) -> str:
        """Выводится название жанра."""
        return self.name


class Title(models.Model):
    """Модель произведения
    Входные переменные:
    category -> При удалении объекта категории Category
    не нужно удалять связанные с этой категорией произведения.
    genre -> При удалении объекта жанра Genre не нужно
    удалять связанные с этим жанром произведения.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    name = models.CharField(
        'Названию произведения',
        max_length=150,
        null=False,
        blank=False,
    )
    year = models.IntegerField(
        'Дата выхода произведения',
        validators=[validator_year]
    )
    description = models.TextField(
        null=True
    )

    class Meta:
        """список сортируется по переменной name."""
        ordering = ('name',)

    def __str__(self) -> str:
        """Выводится имя Title."""
        return f'Названию произведения: {self.name}'


class Review(models.Model):
    """ Модель для отзывов на произведения.
    Отзыв привязан к определенному произведению. На одно произведение
    пользователь может оставить только один отзыв.
    """
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(
        'Дата буликации',
        auto_now_add=True,
        db_index=True
    )
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1,
                'Допустимы значения от 1 до 10'
            ),
            MaxValueValidator(
                10,
                'Допустимы значения от 1 до 10'
            ),
        ]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    class Meta:
        """Список отсортирован по дате публикации."""
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'title',
                    'author'
                ],
                name='unique_review'
            ),
        ]

    def __str__(self) -> str:
        """Отображаются только первые десять символов текста."""
        return self.text[:10]


class Comment(models.Model):
    """ Модель для создания комментариев к отзывам."""
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата буликации',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    class Meta:
        """Список отсортирован по дате публикации."""
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        """Отображаются только первые десять символов текста."""
        return self.text[:10]
