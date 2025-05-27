from rest_framework import serializers

from .models import *


class UserTableSerializer(serializers.ModelSerializer):
    hashed_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserTable
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "hashed_password",
            "email",
            "state",
        ]
