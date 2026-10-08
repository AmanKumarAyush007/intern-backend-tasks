
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Validate and register new users."""

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'role',
        ]
        read_only_fields = ['id']

    def validate_role(self, value):
        """Prevent users from registering as admins."""
        if value == 'admin':
            raise serializers.ValidationError(
                "You cannot register as an admin."
            )
        return value

    def create(self, validated_data):
        """Create a user with a securely hashed password."""
        return User.objects.create_user(**validated_data)
