from django.urls import path
from .views import DhtCreateView

urlpatterns = [
    path("post/", DhtCreateView.as_view(), name="dht-post"),
]
