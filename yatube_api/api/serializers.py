from rest_framework import serializers
from posts.models import Post, Group, Comment, Follow
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели постов.
    """
    author = serializers.StringRelatedField()
    image = serializers.ImageField(required=False)

    class Meta:
        fields = '__all__'
        read_only_fields = ('id', 'author', 'pub_date',)
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели групп.
    """
    class Meta:
        fields = '__all__'
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели комментариев.
    """
    author = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
        read_only_fields = ('id', 'author', 'post', 'created')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели подписок.
    """
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('user',)
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError("Невозможно подписаться на себя")
        return data
