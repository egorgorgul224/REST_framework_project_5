from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализация модели User. Предоставлен доступ доступ к полям: first_name, last_name, city, phone."""

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone", "city"]


class RegisterUserSerializer(serializers.ModelSerializer):
    """Сериализация модели User для регистрации/создания пользователя. Предоставлен доступ к полям: email, password."""

    class Meta:
        model = User
        fields = ["email", "password"]
