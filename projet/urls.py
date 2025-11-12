
from django.contrib import admin
from django.urls import path, include

from DHT import api, views

urlpatterns = [
    path("api", api.Dlist, name='json'),
    path("api/post", api.Dhtviews.as_view(), name='json'),
    path("", views.dashboard, name="dashboard"),
    path("latest/", views.latest_json, name="latest_json"),
]