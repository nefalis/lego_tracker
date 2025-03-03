from django.contrib.auth.models import User
from rest_framework import serializers
from .models import LegoSet


class LegoSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegoSet
        fields = ['id', 'name', 'lego_id', 'quantity', 'price']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Créer un utilisateur avec un mot de passe sécurisé"""
        user = User.objects.create_user(**validated_data)
        return user
