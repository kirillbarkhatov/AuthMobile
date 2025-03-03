from rest_framework import serializers

from .models import User


class InvitedUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователей, которых пригласил текущий пользователь.
    """

    class Meta:
        model = User
        fields = ["id", "phone"]


class InvitedByUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для информации о пригласившем пользователе.
    """

    class Meta:
        model = User
        fields = ["id", "phone", "invite_code"]  # Добавляем нужные поля


class UserSerializer(serializers.ModelSerializer):
    """
    Основной сериализатор пользователя.
    Включает данные о пригласившем пользователе и приглашённых пользователях.
    """

    invited_users = InvitedUserSerializer(many=True, read_only=True)
    invited_by_user = InvitedByUserSerializer(
        source="invited_by", read_only=True
    )  # Добавляем вложенный объект

    class Meta:
        model = User
        fields = [
            "id",
            "phone",
            "invite_code",
            "invited_by_user",
            "created_at",
            "invited_users",
        ]


class RegisterSerializer(serializers.Serializer):
    """
    Сериализатор для регистрации/авторизации пользователя.
    """

    phone = serializers.CharField(max_length=15)
    invited_by = serializers.CharField(
        max_length=6, required=False, allow_blank=True
    )  # Поле необязательное


class VerifyCodeSerializer(serializers.Serializer):
    """
    Сериализатор для проверки кода подтверждения.
    """

    phone = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=4)
