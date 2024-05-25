from django.shortcuts import render
from .models import EVChargingLocation
from django.http import JsonResponse
from geopy.distance import geodesic

# Create your views here.
def index(request):
    stations = list(EVChargingLocation.objects.values('latitude', 'longitude'))
    context = {'stations': stations}
    return render(request, 'index.html', context)

def nearest_stations(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    user_location = latitude, longitude
    stations_distances = {}

    for station in EVChargingLocation.objects.all():
        station_location = station.latitude, station.longitude
        distance =  geodesic(user_location, station_location).km
        stations_distances[distance] = station_location    

    minimum_distance = min(stations_distances)
    station_cordinates = stations_distances[minimum_distance]


    

    context = {
        'cordiantes': station_cordinates,
        'distance': minimum_distance,
    }

    return JsonResponse(context)

