from rest_framework import serializers

from api.serializers.custom_fields import Base64ImageField
from api.serializers.tags import TagSerializer
from recipes.models import Recipe, IngredientInRecipe, Tag
from users.models import User


class AuthorRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для автора рецепта"""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для промежуточной модели IngredientInRecipe"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)
        extra_kwargs = {
            'id': {'required': True},
            'amount': {'required': True}
        }


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe."""
    author = serializers.SerializerMethodField(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time',)

    def get_author(self, obj):
        return AuthorRecipeSerializer(obj.author).data

    def get_ingredients(self, obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients, many=True).data

    def get_tags(self, obj):
        tags = Tag.objects.filter(recipes=obj)
        return TagSerializer(tags, many=True).data


class RecipeCreateSerializer(RecipeSerializer):
    """Сериализатор для создания и изменения рецептов"""
    image = Base64ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time', 'author',)
        extra_kwargs = {
            'ingredients': {'required': True},
            'tags': {'required': True}
        }

    def validate(self, data):
        ingredients = self.context['request'].data.get('ingredients', None)
        tags = self.context['request'].data.get('tags', None)
        if ingredients is None:
            raise serializers.ValidationError('ingredients: Обязательное поле')
        if tags is None:
            raise serializers.ValidationError('tags: Обязательное поле')
        data.update({
            'author': self.context['request'].user,
            'ingredients': ingredients,
            'tags': tags
        })
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = super().create(validated_data)
        for ingredient in ingredients:
            IngredientInRecipe.objects.create(
                ingredient_id=ingredient['id'],
                recipe_id=recipe.id,
                amount=ingredient['amount'],
            )
        return recipe
