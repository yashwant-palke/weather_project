from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("weather", views.weather, name="weather"),
    path("geo", views.get_coordinates, name="geo"),
]