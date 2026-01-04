# views.py
# views.py
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .models import Dht11
from django.shortcuts import render
from .models import Dht11 # Assurez-vous d'importer le modèle Dht11
from django.utils import timezone
import csv
from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Dht11 ,Incident
from django.utils import timezone
from rest_framework.response import Response
from django.core.mail import send_mail
from .models import Dht11
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import Incident, OperatorProfile

def dashboard(request):
    # Rend juste la page; les données sont chargées via JS
    return render(request, "dashboard.html")

def latest_json(request):
    # Fournit la dernière mesure en JSON (sans passer par api.py)
    last = Dht11.objects.order_by('-dt').values('temp', 'hum', 'dt').first()
    if not last:
        return JsonResponse({"detail": "no data"}, status=404)
    return JsonResponse({
        "temperature": last["temp"],
        "humidity":    last["hum"],
        "timestamp":   last["dt"].isoformat()
    })

def home(request):
    return redirect("dashboard")

def table(request):
    derniere_ligne = Dht11.objects.last()
    derniere_date = Dht11.objects.last().dt
    delta_temps = timezone.now() - derniere_date
    difference_minutes = delta_temps.seconds // 60
    temps_ecoule = ' il y a ' + str(difference_minutes) + ' min'
    if difference_minutes > 60:
     temps_ecoule = 'il y ' + str(difference_minutes // 60) + 'h' + str(difference_minutes % 60) + 'min'
    valeurs = {'date': temps_ecoule, 'id': derniere_ligne.id, 'temp': derniere_ligne.temp, 'hum':
    derniere_ligne.hum}
    return render(request, 'value.html', {'valeurs': valeurs})


def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht11_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Temperature', 'Humidity'])

    data = Dht11.objects.all().order_by('dt')

    for d in data:
        writer.writerow([
            d.dt.strftime("%Y-%m-%d %H:%M:%S"),
            d.temp,
            d.hum
        ])

    return response

def graphique(request):
    return render(request, 'Chart.html')

#pour récupérer les valeurs de température et humidité de dernier 24h
# et envoie sous forme JSON
def chart_data_jour(request):
    dht = Dht11.objects.all()
    now = timezone.now()
    # Récupérer l'heure il y a 24 heures
    last_24_hours = now - timezone.timedelta(hours=24)
    # Récupérer tous les objets de Module créés au cours des 24 dernières heures
    dht = Dht11.objects.filter(dt__range=(last_24_hours, now))
    data = {
    'temps': [Dt.dt for Dt in dht],
    'temperature': [Temp.temp for Temp in dht],
    'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)



#pour récupérer les valeurs de température et humidité de dernier semaine
# et envoie sous forme JSON
def chart_data_semaine(request):
    dht = Dht11.objects.all()
    # calcul de la date de début de la semaine dernière
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
    print(datetime.timedelta(days=7))
    print(date_debut_semaine)
    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)
    data = {
    'temps': [Dt.dt for Dt in dht],
    'temperature': [Temp.temp for Temp in dht],
    'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)


#pour récupérer les valeurs de température et humidité de dernier moins
# et envoie sous forme JSON
def chart_data_mois(request):
    dht = Dht11.objects.all()
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
    print(datetime.timedelta(days=30))
    print(date_debut_semaine)
    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)
    data = {
    'temps': [Dt.dt for Dt in dht],
    'temperature': [Temp.temp for Temp in dht],
    'humidity': [Hum.hum for Hum in dht]
    }

    
    return JsonResponse(data)

# views.py
def chart_data(request):
    dht = Dht11.objects.all().order_by('-dt')[:10]  # dernières 10 mesures
    data = {
        'temps': [obj.dt for obj in dht],
        'temperature': [obj.temp for obj in dht],
        'humidity': [obj.hum for obj in dht],
    }
    return JsonResponse(data)

@csrf_exempt
def post_dht(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            temp = float(data.get("temp", 0))
            hum = float(data.get("hum", 0))
            
            dht = Dht11(temp=temp, hum=hum, dt=timezone.now())
            dht.save()
            
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)

def chart_data_all(request):
    dht = Dht11.objects.all().order_by('dt')  # toutes les données
    data = {
        'temps': [obj.dt for obj in dht],
        'temperature': [obj.temp for obj in dht],
        'humidity': [obj.hum for obj in dht],
    }
    return JsonResponse(data)

def post(self, request):
        temp = float(request.data.get("temp"))
        hum = float(request.data.get("hum"))

        # Enregistrer la donnée brute
        d = Dht11.objects.create(temp=temp, hum=hum)

        # Zone normale : 2°C < T < 8°C
        if 2 < temp < 8:
            # Clôturer l'incident en cours si existe
            incident = Incident.objects.filter(resolu=False).last()
            if incident:
                incident.resolu = True
                incident.date_fin = timezone.now()
                incident.save()

        else:
            # Création / mise à jour de l'incident
            incident, created = Incident.objects.get_or_create(
                resolu=False,
                defaults={
                    'date_debut': timezone.now(),
                    'temperature_max': temp,
                    'compteur_alerte': 1
                }
            )

            if not created:
                incident.temperature_max = max(incident.temperature_max, temp)
                incident.compteur_alerte += 1

            incident.save()

            # ⚠️ ALERTE EMAIL SI compteur == 3, 6, 10...
            if incident.compteur_alerte in [3, 6, 10]:
                send_mail(
                    "Alerte DHT11",
                    f"Température anormale : {temp}°C.\nCompteur : {incident.compteur_alerte}",
                    "ton_mail@gmail.com",
                    ["destinataire@gmail.com"],
                    fail_silently=True
                )

        return Response({"status": "OK", "saved": True})

@csrf_exempt
def push_data(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            temperature = body.get("temperature")
            humidity = body.get("humidity")

            if temperature is None or humidity is None:
                return JsonResponse({"error": "temperature and humidity are required"}, status=400)

            # save to DB
            Dht11.objects.create(
                temperature=temperature,
                humidity=humidity
            )

            return JsonResponse({"message": "Data stored successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)




@staff_member_required
def admin_dashboard(request):
    last_dht = Dht11.objects.order_by('-dt').first()
    incidents = Incident.objects.order_by('-date_debut')[:5]

    context = {
        "temperature": last_dht.temp if last_dht else None,
        "humidity": last_dht.hum if last_dht else None,
        "incidents": incidents
    }
    return render(request, "admin/dashboard.html", context)
@staff_member_required
def incident_list(request):
    incidents = Incident.objects.all().order_by('-date_debut')
    return render(request, "admin/incidents.html", {
        "incidents": incidents
    })
@staff_member_required
def incident_detail(request, incident_id):
    incident = Incident.objects.get(id=incident_id)

    return render(request, "admin/incident_detail.html", {
        "incident": incident
    })



def chart_temperature(request):
    temps = Dht11.objects.order_by('-dt')[:50]  # dernier 50 par date
    context = {
        'data': temps,
        'type': 'Température'
    }
    return render(request, 'chartGen.html', context)

def chart_humidity(request):
    hums = Dht11.objects.order_by('-dt')[:50]
    context = {
        'data': hums,
        'type': 'Humidité'
    }
    return render(request, 'humchart.html', context)

@csrf_exempt
def update_incident(request, pk):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    try:
        data = json.loads(request.body)
        incident = Incident.objects.get(id=pk)

        incident.commentaire = data.get("commentaire", incident.commentaire)
        incident.accuse_reception = data.get(
            "accuse_reception",
            incident.accuse_reception
        )

        resolu = data.get("resolu", incident.resolu)

        # 🔥 logique métier CRUCIALE
        if resolu and not incident.resolu:
            incident.resolu = True
            incident.date_fin = timezone.now()
            incident.operateur = request.user if request.user.is_authenticated else None

        incident.save()

        return JsonResponse({"message": "Incident mis à jour avec succès"})

    except Incident.DoesNotExist:
        return JsonResponse({"error": "Incident introuvable"}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "Erreur serveur"}, status=500)
    
def incident_detail(request, incident_id):
    incident = get_object_or_404(Incident, id=incident_id)

    return render(request, "incident_detail.html", {
        "incident": incident
    })