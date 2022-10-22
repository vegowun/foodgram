from django.contrib import admin

from recipes.ingredients.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    # list_display = ()
    pass
