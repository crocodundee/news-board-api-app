from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user"""

    class Meta:
        model = get_user_model()
        fields = ("username", "password", "email")
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8},
            "email": {"required": False},
        }

    def create(self, validated_data):
        """Create a new user"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for token created for user authentication"""

    username = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate user"""
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
        )

        if not user:
            msg = "Unable authenticate with provided credentials"
            raise serializers.ValidationError(msg, code="authenticate")

        attrs["user"] = user
        return attrs
