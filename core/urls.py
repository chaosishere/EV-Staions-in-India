from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-nearest-station', views.nearest_stations, name='get_nearest_stations')
]
