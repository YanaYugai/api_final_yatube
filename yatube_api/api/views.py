from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsOwnerOrReadOnly
from api.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from posts.models import Comment, Group, Post, User


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        IsOwnerOrReadOnly,
    ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer: PostSerializer) -> None:
        """Cохранение нового экземпляра объекта.

        Args:
            serializer(PostSerializer): Сериаоизатор модели POst.

        """
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Сomment."""

    permission_classes = [
        IsOwnerOrReadOnly,
    ]
    serializer_class = CommentSerializer

    def get_post(self) -> Post:
        """Получение текущего поста.

        Returns:
            Post: Экземпляр модели Post.

        """
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self) -> Comment:
        """Получение queryset co всеми комментариями.

        Returns:
            Comment: Экземпляр модели Comment.

        """
        return self.get_post().comments.all()

    def perform_create(self, serializer: CommentSerializer) -> None:
        """Cохранение нового экземпляра объекта.

        Args:
            serializer(CommentSerializer): Сериализатор модел Comment.

        """
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для модели Follow."""

    serializer_class = FollowSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self) -> User:
        """Получение queryset co всеми подписками пользователей.

        Returns:
            User: Экземпляр модели User.

        """
        user = get_object_or_404(User, username=self.request.user.username)
        return user.follower.all()

    def perform_create(self, serializer: FollowSerializer) -> None:
        """Cохранение нового экземпляра объекта.

        Args:
            serializer(FollowSerializer): Сериализатор модел Follow.

        """
        serializer.save(user=self.request.user)
