from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import Dht11, Incident
from .serializers import DHT11serialize
from .utils import send_telegram
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
@api_view(['POST'])
def push_data(request):
    # Debug start
    print("\n" + "="*60)
    print("DEBUG: push_data endpoint called")
    print("="*60)
    
    # Print request details
    print(f"Method: {request.method}")
    print(f"Content-Type: {request.content_type}")
    
    # Print raw body
    raw_body = request.body.decode('utf-8') if request.body else ""
    print(f"Raw body: {raw_body}")
    
    # Try to parse JSON
    try:
        if raw_body:
            json_data = json.loads(raw_body)
            print(f"Parsed JSON: {json_data}")
        else:
            json_data = {}
            print("Empty request body")
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        return Response({
            "error": "Invalid JSON",
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Extract data - FIRST try request.data (DRF parsed), then json_data
    data_source = request.data if request.data else json_data
    
    print(f"Data source keys: {list(data_source.keys()) if hasattr(data_source, 'keys') else 'No keys'}")
    
    # Get values - try both possible field names
    temp = None
    hum = None
    
    # Try from request.data (DRF parsed)
    if hasattr(data_source, 'get'):
        # First try 'temp'/'hum' (Django model names)
        temp = data_source.get('temp')
        hum = data_source.get('hum')
        
        print(f"After trying 'temp'/'hum': temp={temp}, hum={hum}")
        
        # If not found, try Arduino field names
        if temp is None:
            temp = data_source.get('temperature')
        if hum is None:
            hum = data_source.get('humidity')
            
        print(f"After trying 'temperature'/'humidity': temp={temp}, hum={hum}")
    
    # If still None, try direct attribute access
    if temp is None and hasattr(data_source, 'temp'):
        temp = data_source.temp
    if hum is None and hasattr(data_source, 'hum'):
        hum = data_source.hum
    
    print(f"Final extracted values: temp={temp} (type: {type(temp)}), hum={hum} (type: {type(hum)})")
    
    # Check if data is missing
    if temp is None or hum is None:
        print("ERROR: Missing temperature or humidity data")
        return Response({
            "error": "Données manquantes",
            "details": f"temp={temp}, hum={hum}",
            "received_data": dict(data_source) if hasattr(data_source, 'items') else str(data_source)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Convert to float
    try:
        temp_float = float(temp)
        hum_float = float(hum)
        print(f"Converted to float: temp={temp_float}, hum={hum_float}")
    except (ValueError, TypeError) as e:
        print(f"ERROR: Conversion failed: {e}")
        return Response({
            "error": "Température ou humidité non valide",
            "details": f"temp='{temp}', hum='{hum}'",
            "conversion_error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Save to database
    print(f"Creating Dht11 object with temp={temp_float}, hum={hum_float}")
    
    try:
        # Method 1: Direct object creation
        instance = Dht11.objects.create(temp=temp_float, hum=hum_float)
        print(f"SUCCESS: Instance created - id={instance.id}, temp={instance.temp}, hum={instance.hum}")
        
    except Exception as e:
        print(f"ERROR creating instance: {e}")
        # Method 2: Try with serializer
        try:
            serializer = DHT11serialize(data={"temp": temp_float, "hum": hum_float})
            if serializer.is_valid():
                instance = serializer.save()
                print(f"SUCCESS via serializer: Instance created - id={instance.id}")
            else:
                print(f"Serializer errors: {serializer.errors}")
                return Response({
                    "error": "Serializer validation failed",
                    "details": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e2:
            print(f"ERROR with serializer too: {e2}")
            return Response({
                "error": "Database error",
                "details": str(e2)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Create incident if temperature is too low
    if temp_float <= 2:
        try:
            Incident.objects.create(
                date_debut=instance.dt,
                temperature_max=temp_float,
                compteur_alerte=1,
                resolu=False,
                commentaire="Automatique",
                accuse_reception=False
            )
            print("Incident created for low temperature")
        except Exception as e:
            print(f"Error creating incident: {e}")
    
    # Success response
    response_data = {
        "message": f"Données ajoutées avec succès",
        "id": instance.id,
        "temp": instance.temp,
        "hum": instance.hum,
        "dt": instance.dt,
        "debug": {
            "received": {
                "temp": temp,
                "hum": hum
            },
            "saved": {
                "temp": instance.temp,
                "hum": instance.hum
            }
        }
    }
    
    print(f"Sending response: {response_data}")
    print("="*60 + "\n")
    
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def incident_status(request):
    incident = Incident.objects.filter(resolu=False).first()
    if incident:
        data = {
            "id": incident.id,
            "date_debut": incident.date_debut,
            "temperature_max": incident.temperature_max,
            "compteur_alerte": incident.compteur_alerte,
        }
    else:
        data = None

    return Response({"incident": data})


@api_view(['GET'])
def Dlist(request):
    all_data = Dht11.objects.all()
    data = DHT11serialize(all_data, many=True).data
    return Response({'data': data})


class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize

    def perform_create(self, serializer):
        instance = serializer.save()
        temp = instance.temp

        # Vérifier que temp n'est pas None
        if temp is not None and temp > 0:
            # 📧 EMAIL
            subject = "⚠️ Température actuelle"
            message = f"La température a atteint {temp:.1f} °C à {timezone.localtime(instance.dt)}."

            try:
                sent = send_mail(
                    subject,
                    message,
                    f"IoT Project | Souhil Boullil | <{settings.EMAIL_HOST_USER}>",
                    [""],  # Mettre ici ton email
                    fail_silently=False,
                )
                print("✅ Email envoyé :", sent)
            except Exception as e:
                print("❌ Erreur email :", e)

            # 📲 TELEGRAM
            try:
                send_telegram(f"⚠️ DHT11 ALERT\nTempérature: {temp:.1f} °C\nDate: {instance.dt}")
            except Exception as e:
                print("❌ Erreur Telegram :", e)