from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализация модели User. Предоставлен доступ доступ к полям: first_name, last_name, city, phone, tg_chat_id."""

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone", "city", "tg_chat_id"]


class UserMinInfoSerializer(serializers.ModelSerializer):
    """Сериализация модели User для просмотра минимальной информации о пользователе, если пользователь не является
    админом. Предоставлен доступ к полям: email, first_name, city, date_joined."""

    class Meta:
        model = User
        fields = ["email", "first_name", "city", "date_joined"]


class RegisterUserSerializer(serializers.ModelSerializer):
    """Сериализация модели User для регистрации/создания пользователя. Предоставлен доступ к полям: email, password."""

    class Meta:
        model = User
        fields = ["email", "password"]
