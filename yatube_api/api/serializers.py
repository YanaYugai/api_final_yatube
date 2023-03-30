from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = SlugRelatedField(slug_field='username', read_only=True)
    group = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Group.objects.all(),
    )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    user = SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username',
    )
    following = SlugRelatedField(
        queryset=User.objects.all(), slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=('user', 'following'),
            ),
        ]

    def validate(self, data):
        if self.context['request'].user != data.get('following'):
            return data
        raise serializers.ValidationError('Нельзя подписаться на себя')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        fields = '__all__'
        model = Group
