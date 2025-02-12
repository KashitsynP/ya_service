from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    id = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SignInSerializer(serializers.Serializer):
    """SignIn Serializer."""

    id = serializers.CharField()
    password = serializers.CharField(write_only=True, required=True)


class LogoutSerializer(serializers.Serializer):
    """Logout serializer."""

    refresh = serializers.CharField()
    all = serializers.BooleanField(default=False)  # Выход со всех устройств


class UserInfoSerializer(serializers.ModelSerializer):
    """Serializer for user information."""

    class Meta:
        model = User
        fields = ["id", "id_type"]
