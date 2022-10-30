from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from recipes.models import Follow
from users.models import User


class UserGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных о пользователя. """
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed',)

    def get_is_subscribed(self, value):
        """Подписан ли текущий пользователь на автора рецепта."""
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return Follow.objects.filter(user=request.user, author=value).exists()


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя. """

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

    def validate(self, data):
        """
        Проверка пароля требованиям у создаваемого пользователя.
        :param data: входяшие данные.
        :return: данные о создаваемом пользователе.
        """
        try:
            validate_password(data['password'])
        except ValidationError as error:
            error = '\n'.join(error)
            raise serializers.ValidationError({'detail': f'Пароль не удовлетворяет требованиям!\n {error}'})
        return data

    def create(self, validated_data):
        """Создание пользователя."""
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        password = validated_data['password']
        user.set_password(validated_data['password'])
        user.save()
        return user
