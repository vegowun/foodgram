from operator import itemgetter

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


class RecipeCreateEditSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и изменения рецептов"""
    image = Base64ImageField(
        max_length=None, use_url=True,
    )
    ingredients = IngredientInRecipeSerializer(source="ingredient_amount", many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time')
        extra_kwargs = {
            'ingredients': {'required': True},
            'tags': {'required': True}
        }

    def validate(self, data):
        data.pop('ingredient_amount')
        data.update({
            'author': self.context['request'].user,
            'ingredients': self.context['request'].data['ingredients']
        })
        return data

    @staticmethod
    def create_ingredients_in_recipe(recipe_id, ingredients):
        for ingredient in ingredients:
            IngredientInRecipe.objects.create(
                ingredient_id=ingredient['id'],
                recipe_id=recipe_id,
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = super().create(validated_data)
        self.create_ingredients_in_recipe(recipe.id, ingredients)
        return recipe

    def update(self, instance, validated_data):
        if instance.author != validated_data['author']:
            raise serializers.ValidationError({'detail': 'У вас недостаточно прав для выполнения данного действия.'})
        new_ingredients = validated_data.pop('ingredients')
        recipe = super().update(instance, validated_data)
        old_ingredients_objects = IngredientInRecipe.objects.filter(recipe=instance.id)
        old_ingredients = [
            {
                'id': old_ingredient.ingredient_id,
                'amount': old_ingredient.amount
            } for old_ingredient in old_ingredients_objects
        ]
        if sorted(old_ingredients, key=itemgetter('id')) != sorted(new_ingredients, key=itemgetter('id')):
            old_ingredients_objects.delete()
            self.create_ingredients_in_recipe(instance.id, new_ingredients)
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data
