""" Спринт 10. Проект YaMDb
Авторы:
        Амирхан Понежев
        Вадим Стрига
        Андрес Парра
Студенты факультета Бэкенд. Когорта 14+

Основная функция serializers.py:
Сериализаторы используют модели из приложения reviews,
чтобы API имел доступ к базе данных для выполнения CRUD.
Сериализаторы следующие:
        1 - CategorySerializer
        2 - CommentSerializer
        3 - GenreSerializer
        4 - ReviewSerializer
        5 - UserSerializer
        6 - UserEditSerializer
        7 - TitleCreateSerializer
        8 - TitleSerializer
        9 - RegistrationSerializer
        10 - TokenJWTSerializer
"""
from rest_framework import serializers, validators

from reviews.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id')
        ).exists():
            raise serializers.ValidationError(
                'На одно произведение можно оставить только один отзыв.')
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""
    username = serializers.CharField(
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all()
            )
        ],
    )
    email = serializers.EmailField(
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all()
            )
        ],
    )

    class Meta:
        model = User
        fields = ("username", "email",
                  "first_name", "last_name",
                  "bio", "role")


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        read_only_fields = ('role',)


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания модели Title."""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title."""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.FloatField(default=None)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'rating', 'description', 'genre', 'category')


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор процесса регистрации пользователей."""
    username = serializers.CharField(
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all()
            )
        ]
    )
    email = serializers.EmailField(
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all()
            )
        ]
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                "Username 'me' is not valid"
            )
        return value

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenJWTSerializer(serializers.Serializer):
    """Сериализатор для генерации кода токена JWT для пользователя.

    Входные переменные:
    username -> имя пользователя, зарегистрированного на платформе YamDb.
    confirmation_code -> код подтверждения, который был отправлен на
                         почту пользователя.
    """
    username = serializers.CharField(
        max_length=150
    )
    confirmation_code = serializers.CharField()
