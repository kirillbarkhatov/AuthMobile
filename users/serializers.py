from rest_framework import serializers
from .models import User


class InvitedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone"]


class UserSerializer(serializers.ModelSerializer):
    invited_users = InvitedUserSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ["id", "phone", "invite_code", "invited_by", "created_at", "invited_users"]


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=4)
