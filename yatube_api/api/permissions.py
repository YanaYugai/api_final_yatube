from typing import Any, Union

from rest_framework import permissions

from posts.models import Comment, Post


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешение редактирования только владельцам."""

    def has_permission(self, request, view) -> bool:
        """Проверка прав пользователя.

        Args:
            bool: Возвращаемое зачение. True - функция сработала удачно,
        иначе False.

        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(
        self,
        request,
        _: Any,
        obj: Union[Post, Comment],
    ) -> bool:
        """Проверка прав пользователя на доступ к объекту.

        Args:
            obj(Union[Post, Comment]): Экземляр класса POst, Comment.
        Returns:
            bool: Возвращаемое зачение. True - функция сработала удачно,
        иначе False.

        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
