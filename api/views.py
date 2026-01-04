from rest_framework import generics
from django.core.mail import send_mail
from django.conf import settings
from .models import Dht11
from .serializers import DHT11serialize
from .utils import send_telegram


class DhtCreateView(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize

    def perform_create(self, serializer):
        instance = serializer.save()

        temp = instance.temp
        humidity = instance.humidity

        if temp > 25:
            # 📧 EMAIL
            subject = "⚠️ Alerte DHT11"
            message = (
                f"⚠️ Température élevée détectée\n\n"
                f"🌡 Température : {temp} °C\n"
                f"💧 Humidité : {humidity} %\n"
                f"🕒 Date : {instance.dt}"
            )

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ["luciferbowlil@gmail.com"],
                fail_silently=False,
            )

            # 📲 TELEGRAM
            send_telegram(
                f"⚠️ DHT11 ALERT\n🌡 {temp}°C\n💧 {humidity}%"
            )
