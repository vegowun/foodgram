from django.urls import include, path
from rest_framework import routers

from api.views.ingredients import IngredientViewSet
from api.views.recipes import RecipeViewSet
from api.views.subscriptions import SubscribeViewSet, SubscriptionsViewSet
from api.views.tags import TagViewSet

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register(
    r'users/subscriptions',
    SubscriptionsViewSet, basename='subscriptions'
)
router.register(
    r'users/(?P<id>[\d]+)/subscribe',
    SubscribeViewSet, basename='subscribe'
)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
