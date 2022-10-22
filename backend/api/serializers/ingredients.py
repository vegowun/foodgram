from rest_framework import serializers

from recipes.ingredients.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Серилазитор для модели Ingredient"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
