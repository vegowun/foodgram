from rest_framework import serializers

from recipes.models import Recipe, IngredientInRecipe


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для промежуточной модели IngredientInRecipe"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe."""
    ingredients = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'ingredients', 'tags', 'image', 'cooking_time',)

    def get_ingredients(self, obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients, many=True).data


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и изменения рецептов"""
    pass
