import requests
import json
import re
import geopy.distance
from datetime import datetime, timedelta
from django.utils import timezone

def fetch_location(location_name_raw):
    # Clean incoming data
    location_name_clean = re.sub('[^a-zA-Z]+', '', location_name_raw)
    location_lower = location_name_clean.lower()

    params = {
        'q': location_lower,
        'maxRows': 10,
        'username': 'dimagi'
    }

    data = {}

    # Try and get data from external API
    try:
        url = 'http://api.geonames.org/searchJSON'
        response = requests.get(url, params=params)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            entry = response_data['geonames'][0]

            data = {
                'lat': entry['lat'],
                'lng': entry['lng'],
                'country_name': entry['countryName']
            }
    except Exception as e:
        print("Exception retrieving from API", e)

    return data

# Checks that the distance traveled over the given timespan until now is valid
# (i.e.) User couldn't have had an average speed of 300km/h over the last 3 days
def validate_distance(coords_1, coords_2, last_time):
    dist = geopy.distance.geodesic(coords_1, coords_2).km
    
    time_diff = timezone.now() - last_time
    seconds_per_day = 3600
    time_diff_hours = time_diff.total_seconds() / seconds_per_day
    speed = dist / time_diff_hours  # Speed is in km/h
    
    max_speed = 120 # Max speed a user can go driving constantly in a car (km/h)
    print('Movement speed is', speed)

    return speed <= max_speed

