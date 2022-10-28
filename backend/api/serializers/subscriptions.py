from rest_framework import serializers

from api.serializers.recipes import AuthorRecipeSerializer, RecipesShortInfo
from recipes.models import Follow, Recipe
from users.models import User


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
            'recipes': RecipesShortInfo(author_recipes, many=True).data,
            'recipes_count': author_recipes.count()
        })
        return data
