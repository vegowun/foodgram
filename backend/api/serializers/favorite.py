from rest_framework import serializers

from api.serializers.recipes import RecipesShortInfo
from recipes.models import Recipe, Favorite


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
        """
        Валидация входящих данных.
        :param data: данные
        :return: обновленные данные, содержащие пользователя и рецепт
        """
        user_id = self.context.get('request').user.id
        recipe_id = self.context.get('request').parser_context.get('kwargs').get('id')
        if Favorite.objects.filter(user=user_id, recipe=recipe_id).exists():
            raise serializers.ValidationError({'detail': 'Уже добавлен в избранное.'})
        data.update({
            'user': self.context.get('request').user,
            'recipe': Recipe.objects.get(pk=int(recipe_id))
        })
        return data

    def create(self, validated_data):
        """
        Создание объекта избранного с добавлением рецепту 1 для отслеживания количества добавлений в избранное.
        :param validated_data: провалидированные данные
        :return: созданный объект подписки
        """
        favorite = super().create(validated_data)
        validated_data['recipe'].favorite_count += 1
        validated_data['recipe'].save()
        return favorite

    def to_representation(self, instance):
        """Ответ в виде короткой информации о рецепте."""
        return RecipesShortInfo(instance.recipe).data
