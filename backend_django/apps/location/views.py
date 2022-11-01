from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, CreateAPIView

from .utils import fetch_location, validate_distance, extract_sms
from rest_framework import status
from rest_framework.response import Response

from django.db.models import Q
from .models import LocationRecord
from .serializers import LocationRecordSerializer

from datetime import datetime
import requests

class LocationRecordListCreateAPIView(ListCreateAPIView):
    queryset = LocationRecord.objects.all().order_by('-location_date')
    serializer_class = LocationRecordSerializer

    def post(self, request, *args, **kwargs):
        # Check if we are dealing with an SMS request
        if 'message' in request.data:
            data = extract_sms(request.data)
            request.data['email'] = data['email']
            request.data['city_name'] = data['location']

        # Make sure we have valid POST data
        if 'email' not in request.data or 'city_name' not in request.data:
            print("No email/location given")
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

    def get(self, request, *args, **kwargs):
        # Add filters, if requested
        q = Q()
        if 'email' in request.GET:
            q &= Q(email__icontains=request.GET['email'])
            print("Querying with", request.GET['email'])

        if 'from_date' in request.GET:
            try:
                from_date_str = request.GET['from_date']
                from_date = datetime.strptime(from_date_str, "%Y-%m-%dT%H:%M")
                q &= Q(location_date__gte=from_date)
            except Exception as e:
                print("Failed processing from date", e)

        if 'to_date' in request.GET:
            try:
                to_date_str = request.GET['to_date']
                to_date = datetime.strptime(to_date_str, "%Y-%m-%dT%H:%M")
                q &= Q(location_date__lte=to_date)
            except Exception as e:
                print("Failed processing to date", e)

        locations = LocationRecord.objects.filter(q)
        serializer = LocationRecordSerializer(locations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
