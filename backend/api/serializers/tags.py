from rest_framework import serializers

from recipes.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Серилазитор для модели Tag"""

    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')
