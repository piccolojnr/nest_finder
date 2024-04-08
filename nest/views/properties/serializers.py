# serializers.py
from nest.models import Property
from rest_framework import serializers


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"


class PropertyMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ["id", "title", "price", "status"]
