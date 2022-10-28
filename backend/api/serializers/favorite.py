from rest_framework import serializers

from api.serializers.recipes import AuthorRecipeSerializer, RecipesShortInfo
from recipes.models import Follow, Recipe, Favorite
from users.models import User


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов."""
    user = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Favorite
        fields = ('user',)

    def validate(self, data):
        user_id = self.context.get('request').user.id
        recipe_id = self.context.get('request').parser_context.get('kwargs').get('id')
        if Favorite.objects.filter(user=user_id, recipe=recipe_id).exists():
            raise serializers.ValidationError({'detail': 'Уже добавлен в избранное.'})
        data.update({
            'user': self.context.get('request').user,
            'recipe': Recipe.objects.get(pk=int(recipe_id))
        })
        return data

    def to_representation(self, instance):
        return RecipesShortInfo(instance.recipe).data
