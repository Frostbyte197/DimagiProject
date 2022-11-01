from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .utils import fetch_location, validate_distance
from rest_framework import status
from rest_framework.response import Response

from .models import LocationRecord
from .serializers import LocationRecordSerializer

class LocationRecordListCreateAPIView(ListCreateAPIView):
    queryset = LocationRecord.objects.all()
    serializer_class = LocationRecordSerializer

    def post(self, request, *args, **kwargs):
        # Need city name for location calculations and API request
        if 'city_name' not in request.data:
            print("No city name given")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Fetch location from external API based on user's location
        new_location_data = fetch_location(request.data['city_name'])
        request.data['lat'] = new_location_data['lat']
        request.data['lng'] = new_location_data['lng']
        request.data['country_name'] = new_location_data['country_name']

        # Validate that the user could have realistically moved there
        last_location = LocationRecord.objects.filter(email=request.data['email']).order_by('-location_date')
        if last_location:
            last_location_data = last_location.first()
            if not validate_distance(
                (last_location_data.lat, last_location_data.lng), 
                (new_location_data['lat'], new_location_data['lng']),
                last_location_data.location_date
            ):
                print("Unrealistic movement speed")
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)

