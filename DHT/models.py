from django.db import models
from django.contrib.auth.models import User

class Dht11(models.Model):
    temp = models.FloatField(null=True)
    hum = models.FloatField(null=True)
    dt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"DHT11 #{self.id} - Temp: {self.temp}°C Hum: {self.hum}%"


class Incident(models.Model):
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField(null=True, blank=True)
    temperature_max = models.FloatField(default=0)
    compteur_alerte = models.IntegerField(default=0)
    resolu = models.BooleanField(default=False)
    accuse_reception = models.BooleanField(default=False)
    operateur = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='dht_incidents'
    )
    commentaire = models.TextField(blank=True, null=True)

    # 🔥 nouveau champ pour suivre le dernier incrément
    last_increment = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Incident #{self.id} - {'résolu' if self.resolu else 'actif'}"


class OperatorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='dht_operator_profile'  # 🔥 important pour éviter les clashes
    )
    phone = models.CharField(max_length=20, blank=True)
    is_active_operator = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
