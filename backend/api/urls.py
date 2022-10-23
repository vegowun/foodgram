from django.urls import include, path
from rest_framework import routers

from api.views.ingredients import IngredientViewSet
from api.views.tags import TagViewSet

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', IngredientViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls))
]