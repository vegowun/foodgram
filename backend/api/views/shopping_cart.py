from django.http import FileResponse, HttpResponse
from rest_framework import viewsets, status, renderers, views
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsAuthenticatedUser
from api.serializers.recipes import RecipeSerializer, IngredientInRecipeSerializer
from api.serializers.shopping_cart import ShoppingCartSerializer
from recipes.models import Recipe, ShoppingCart


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """Вьюсет для списка покупок."""

    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticatedUser,)

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        recipe = Recipe.objects.get(pk=int(kwargs['id']))
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            ShoppingCart.objects.get(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            data={'detail': 'Рецепт не добавлен в избранное!'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ShoppingCartDownloadView(views.APIView):
    """Вью для скачивания списка покупок."""
    permission_classes = (IsAuthenticatedUser,)

    def prepare_shopping_cart(self):
        ingredients_recipes = [
            unit.recipe.ingredient_amount.all() for unit in ShoppingCart.objects.filter(user=self.request.user)
        ]
        ingredients_amount = [ing for x in ingredients_recipes for ing in x]
        shopping_ingredients = {}
        for ingredient_amount in ingredients_amount:
            ingredient_name = (
                f'{str(ingredient_amount.ingredient).capitalize()} ({ingredient_amount.ingredient.measurement_unit})'
            )
            if shopping_ingredients.get(ingredient_name):
                shopping_ingredients[ingredient_name] += ingredient_amount.amount
            else:
                shopping_ingredients[ingredient_name] = ingredient_amount.amount
        return shopping_ingredients

    def get(self, *args, **kwargs):
        shopping_ingredients = self.prepare_shopping_cart()
        shopping_list = '\n'.join([f'{name} - {amount}' for name, amount in shopping_ingredients.items()])
        response = HttpResponse(shopping_list, content_type='text/plain; charset=utf8')
        response['Content-Disposition'] = f'attachment; filename="shopping_list.txt"'
        return response
