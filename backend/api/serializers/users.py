from rest_framework import serializers

from recipes.models import Follow
from users.models import User


class UserGetSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed',)

    def get_is_subscribed(self, value):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return Follow.objects.filter(user=request.user, author=value).exists()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password',)
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True, 'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
