from django.urls import include, path
from rest_framework import routers

from api.views.favorite import FavoriteViewSet
from api.views.ingredients import IngredientViewSet
from api.views.recipes import RecipeViewSet
from api.views.shopping_cart import ShoppingCartViewSet, ShoppingCartDownloadView
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
router.register(
    r'recipes/(?P<id>[\d]+)/favorite',
    FavoriteViewSet, basename='favorite'
)
router.register(
    r'recipes/(?P<id>[\d]+)/shopping_cart',
    ShoppingCartViewSet, basename='shopping_cart'
)
app_name = 'api'

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        ShoppingCartDownloadView.as_view(),
        name='download_shopping_cart'
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
