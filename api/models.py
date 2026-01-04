from django.db import models
from django.contrib.auth.models import User

class Incident(models.Model):

    STATUT_CHOICES = [
        ('open', 'Ouvert'),
        ('ack', 'Accusé'),
        ('closed', 'Clos'),
    ]

    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True, blank=True)

    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default='open'
    )

    temperature_max = models.FloatField()
    compteur_alerte = models.IntegerField(default=1)

    operateur = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="incidents"
    )

    commentaire_operateur = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Incident #{self.id} - {self.statut}"

class OperatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    is_active_operator = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
