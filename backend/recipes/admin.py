from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from recipes.models import Tag, Recipe, IngredientInRecipe, Follow, Favorite, ShoppingCart


class RecipeAdminForm(ModelForm):
    def clean_ingredients(self):
        data = self.cleaned_data['ingredients']
        if data is None:
            raise ValidationError('Обязательное поле')
        return self.cleaned_data['ingredients']


class RecipeIngredientChoiceInline(admin.TabularInline):
    model = IngredientInRecipe
    fields = ('ingredient', 'amount',)
    min_num = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'get_str_ingredients',
        'get_str_tags',
        'favorite_count'
    )
    list_filter = ('name', 'author', 'tags')
    inlines = (RecipeIngredientChoiceInline,)
    readonly_fields = ('favorite_count',)
    empty_value_display = '-пусто-'


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)
    list_filter = ('ingredient',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author',)
    list_filter = ('user', 'author',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-пусто-'
