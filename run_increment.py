import time
import os
import django

# config Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iotserver.settings")
django.setup()

from DHT.models import Incident

while True:
    incident = Incident.objects.filter(resolu=False).first()
    if incident:
        incident.compteur_alerte += 1
        incident.save()
        print(f"Compteur incrémenté: {incident.compteur_alerte}")
    time.sleep(60)  # attendre 1 minute


