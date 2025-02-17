from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "invite_code", "invited_by", "created_at"]


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=4)
