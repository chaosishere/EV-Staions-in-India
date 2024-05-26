from django.shortcuts import render
from django.http import JsonResponse
from .models import EVChargingLocation
from geopy.distance import geodesic
import requests
import os
import polyline

# Ensure you have your OpenRouteService API key set in your environment
ORS_API_KEY = os.getenv('ORS_API_KEY')

def index(request):
    stations = list(EVChargingLocation.objects.values('latitude', 'longitude'))
    context = {'stations': stations}
    return render(request, 'index.html', context)

def nearest_station(request):
    latitude = float(request.GET.get('latitude'))
    longitude = float(request.GET.get('longitude'))
    user_location = (latitude, longitude)
    
    stations_distances = {
        geodesic(user_location, (station.latitude, station.longitude)).km: (station.latitude, station.longitude)
        for station in EVChargingLocation.objects.all()
    }

    minimum_distance = min(stations_distances.keys())
    station_coordinates = stations_distances[minimum_distance]

    route = get_route(user_location, station_coordinates)

    print(route)
    decoded_polyline = polyline.decode(route['routes'][0]['geometry'])

    context = {
        'coordinates': station_coordinates,
        'distance': minimum_distance,
        'route': decoded_polyline,
    }

    return JsonResponse(context)

def get_route(start, end):
    headers = {
        'Authorization': f'Bearer {ORS_API_KEY}',
        'Content-Type': 'application/json',
    }

    data = {
        "coordinates": [
            [start[1], start[0]],
            [end[1], end[0]]
        ],
        "format": "json"
    }

    response = requests.post('https://api.openrouteservice.org/v2/directions/driving-car', headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {}