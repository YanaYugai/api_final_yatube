from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from api.permissions import IsOwnerOrReadOnly
from api.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from posts.models import Comment, Group, Post, User


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели `Post`."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer: PostSerializer) -> None:
        """Cохранение нового экземпляра объекта.

        Args:
            serializer: Сериализатор модели `Post`.

        """
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели `Group`."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели `Сomment`."""

    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    serializer_class = CommentSerializer

    def get_post(self) -> Post:
        """Получение текущего поста.

        Returns:
            Экземпляр модели `Post`.

        """
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self) -> Comment:
        """Получение queryset co всеми комментариями.

        Returns:
            Экземпляр модели `Comment`.

        """
        return self.get_post().comments.all()

    def perform_create(self, serializer: CommentSerializer) -> None:
        """Cохранение нового экземпляра объекта.

        Args:
            serializer: Сериализатор модели `Comment`.

        """
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)


class CreateReadViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Базовый класс для вьюсетов."""


class FollowViewSet(CreateReadViewSet):
    """Вьюсет для модели Follow."""

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self) -> User:
        """Получение queryset co всеми подписками пользователей.

        Returns:
            Экземпляр модели `User`.

        """
        return self.request.user.follower.all()

    def perform_create(self, serializer: FollowSerializer) -> None:
        """Cохранение нового экземпляра объекта.

        Args:
            serializer: Сериализатор модели `Follow`.

        """
        serializer.save(user=self.request.user)
