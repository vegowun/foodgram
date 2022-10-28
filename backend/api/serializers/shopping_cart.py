from rest_framework import serializers

from api.serializers.recipes import RecipesShortInfo
from recipes.models import Recipe, Favorite, ShoppingCart


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок."""
    user = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = ShoppingCart
        fields = ('user',)

    def validate(self, data):
        user_id = self.context.get('request').user.id
        recipe_id = self.context.get('request').parser_context.get('kwargs').get('id')
        if ShoppingCart.objects.filter(user=user_id, recipe=recipe_id).exists():
            raise serializers.ValidationError({'detail': 'Уже добавлен в список покупок.'})
        data.update({
            'user': self.context.get('request').user,
            'recipe': Recipe.objects.get(pk=int(recipe_id))
        })
        return data

    def to_representation(self, instance):
        return RecipesShortInfo(instance.recipe).data
