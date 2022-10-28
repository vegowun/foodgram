from django.contrib import admin

from recipes.models import Tag, Recipe, IngredientInRecipe, Follow, Favorite


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'get_str_ingredients',
        'text',
        'cooking_time',
        'image',
        'get_str_tags',
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)
    search_fields = ('ingredient',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author',)
    search_fields = ('user', 'author',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe',)
    search_fields = ('user', 'recipe',)
    empty_value_display = '-пусто-'
