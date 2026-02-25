from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Follow, Group

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username",
                              read_only=True)

    class Meta:
        fields = "__all__"
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field="username")
    post = serializers.SlugRelatedField(read_only=True,
                                        slug_field="id")

    class Meta:
        fields = "__all__"
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True,
                                        slug_field="username")
    following = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
    )

    class Meta:
        fields = "__all__"
        model = Follow

    def validate(self, data):
        user = self.context["request"].user
        following = data.get("following")

        # ПРОВЕРКА 1: Самоподписка (Этого не хватало!)
        if user == following:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя.")

        # ПРОВЕРКА 2: Дубликат
        if Follow.objects.filter(user=user,
                                 following=following).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого автора.")

        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
