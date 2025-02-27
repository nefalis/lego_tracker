from rest_framework import serializers
from .models import LegoSet


class LegoSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegoSet
        fields = ['id', 'name', 'lego_id', 'quantity', 'price']
