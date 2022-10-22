from django.urls import include, path
from rest_framework import routers

from api.views.ingredients import IngredientViewSet

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', IngredientViewSet, basename='recipes')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls))
]