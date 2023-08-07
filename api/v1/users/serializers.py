import email
from django.contrib.auth.password_validation import validate_password

from users.models import User
from rest_framework import serializers
from rest_framework import status


__all__ = ["UserRegisterSerializer", "UserLoginSerializer"]


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "user_type",
            "password",
            "confirm_password",
        )
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def validate(self, attrs: dict):
        """Validate that the two passwords match"""
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError(
                detail={"password": ["Passwords missmatch."]},
                code=status.HTTP_406_NOT_ACCEPTABLE,
            )
        return attrs

    def validate_password(self, value: str):
        if value:
            validate_password(value)
        return value

    def create(self, validated_data: dict):
        user = User(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            email=validated_data["email"],
            user_type=validated_data["user_type"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "user_type",
            "password",
        )
        read_only_fields = ("id", "first_name", "last_name", "email", "user_type")
        extra_kwargs = {
            "password": {"write_only": True},
        }
