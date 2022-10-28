from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers.recipes import AuthorRecipeSerializer
from recipes.models import Tag, Follow, Recipe
from users.models import User


class RecipesAuthorSerializerForSubscription(serializers.ModelSerializer):
    """Сериализатор для отображения рецептов автора в подписке."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки/отписки на/от пользователя."""
    user = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Follow
        fields = ('user',)

    def validate(self, data):
        user_id = self.context.get('request').user.id
        author_id = self.context.get('request').parser_context.get('kwargs').get('id')
        if user_id == author_id:
            raise serializers.ValidationError({'detail': 'Невозможно подписаться на самого себя.'})
        if Follow.objects.filter(user=user_id, author=author_id).exists():
            raise serializers.ValidationError({'detail': 'Уже подписаны.'})
        data.update({
            'user': self.context.get('request').user,
            'author': User.objects.get(pk=author_id)
        })
        return data

    def to_representation(self, instance):
        author = instance.author
        data = AuthorRecipeSerializer(author, context={'request': self.context.get('request')}).data
        author_recipes = Recipe.objects.filter(author=author)
        data.update({
            'recipes': RecipesAuthorSerializerForSubscription(author_recipes, many=True).data,
            'recipes_count': author_recipes.count()
        })
        return data
