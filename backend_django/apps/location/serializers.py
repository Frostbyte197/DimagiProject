from rest_framework import serializers
from .models import LocationRecord


class LocationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationRecord
        fields = '__all__'