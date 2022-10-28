from django_filters import rest_framework as filters

from recipes.models import Recipe


class IngredientsFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )


class RecipesFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )

    class Meta:
        model = Recipe
        fields = ('is_favorited',)

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(favorite__user=user)
        return None
