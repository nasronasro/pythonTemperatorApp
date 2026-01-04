from django.core.management.base import BaseCommand
from django.utils import timezone
from DHT.models import Incident

class Command(BaseCommand):
    help = 'Incrémente le compteur des incidents toutes les minutes'

    def handle(self, *args, **options):
        now = timezone.now()
        incident = Incident.objects.filter(resolu=False).first()
        if not incident:
            self.stdout.write("Aucun incident actif")
            return

        if not incident.last_increment or (now - incident.last_increment).total_seconds() >= 60:
            incident.compteur_alerte += 1
            incident.last_increment = now
            incident.save()
            self.stdout.write(f"Compteur incrémenté à {incident.compteur_alerte} pour l’incident #{incident.id}")
        else:
            self.stdout.write("Pas encore 1 minute écoulée")
