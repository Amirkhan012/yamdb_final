""" Спринт 10. Проект YaMDb
Авторы:
        Амирхан Понежев
        Вадим Стрига
        Андрес Парра
Студенты факультета Бэкенд. Когорта 14+

Основная функция views.py:
как работает API.
Использовались следующие ViewSets:
        1 - TitleViewSet
        2 - UserViewSet
        3 - CategoryViewSet
        4 - GenreViewSet
        5 - ReviewViewSet
        6 - CommentViewSet
        7 - registration (функция для регистрации)
        8 - get_jwttoken_user (функция для получения токена jwt)
"""
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User
from .filters import TitlesFilter
from .permissions import (IsAdmin, IsAdminModeratorOwnerOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegistrationSerializer,
                          ReviewSerializer, TitleCreateSerializer,
                          TitleSerializer, TokenJWTSerializer,
                          UserEditSerializer, UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """Класс связан с моделью Title.
    Можно ли создавать сообщения из API."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Класс связан с моделью User.
    Можно ли создавать сообщения из API."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    lookup_field = "username"

    @action(
        methods=["get", "patch", ],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer
    )
    def users_self_profile(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(
                request.user
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        if request.method == "PATCH":
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(
                raise_exception=True
            )
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Класс связан с моделью Category.
    Можно ли создавать сообщения из API."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Класс связан с моделью Genre.
    Можно ли создавать сообщения из API."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс связан с моделью Review.
    Можно ли создавать сообщения из API."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get("title_id")
        )
        serializer.save(
            title=title,
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Класс связан с моделью Comment.
    Можно ли создавать сообщения из API."""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id"),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id"),
        )
        serializer.save(
            review=review,
            author=self.request.user
        )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def registration(request):
    """Эта функция регистрирует пользователей
    на платформе YamDb"""

    serializer = RegistrationSerializer(
        data=request.data
    )
    serializer.is_valid(
        raise_exception=True
    )
    user = serializer.save()
    code_confirmation_email = default_token_generator.make_token(user)
    send_mail(
        subject=f"Welcome: {user.username} зарегистрируйтесь на YamDb.",
        message=f"Ваш код подтверждения: {code_confirmation_email}",
        from_email=None,
        recipient_list=[user.email]
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_jwttoken_user(request):
    """Эта функция назначает JWT токен пользователю,
    зарегистрированному на платформе YamDb."""

    serializer = TokenJWTSerializer(
        data=request.data
    )
    serializer.is_valid(
        raise_exception=True
    )
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    if default_token_generator.check_token(
        user,
        serializer.validated_data[
            "confirmation_code"]):
        token = AccessToken.for_user(user)
        return Response(
            {"token": str(token)},
            status=status.HTTP_200_OK
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
