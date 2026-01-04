from django.contrib import admin
from .models import Dht11, Incident, OperatorProfile

@admin.register(Dht11)
class Dht11Admin(admin.ModelAdmin):
    list_display = ('id', 'temp', 'hum', 'dt')
    ordering = ('-dt',)


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date_debut',
        'date_fin',
        'temperature_max',
        'compteur_alerte',
        'operateur',
        'resolu',
        'accuse_reception',
    )
    list_filter = ('resolu', 'accuse_reception', 'operateur')
    search_fields = ('operateur__username',)


@admin.register(OperatorProfile)
class OperatorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_active_operator')
    list_filter = ('is_active_operator',)
    search_fields = ('user__username', 'phone')
