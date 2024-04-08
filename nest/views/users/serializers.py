from rest_framework import serializers
from nest.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "profile_picture",
            "contact_information",
            "role",
            "property_owner_profile",
        ]
