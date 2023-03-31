from typing import Union

from rest_framework import permissions
from rest_framework.request import Request

from posts.models import Comment, Post


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешение редактирования только владельцам."""

    def has_object_permission(
        self, request: Request, view: None, obj: Union[Post, Comment],
    ) -> bool:
        """Проверка прав пользователя на доступ к объекту.

        Args:
            request: Запрос пользователя.
            view: Неиспользуемая переменная.
            obj: Экземляр класса `Post`, `Comment`.

        Returns:
            True - функция сработала удачно, иначе False.

        """
        del view
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
        )
