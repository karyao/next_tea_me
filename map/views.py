from django.http import JsonResponse
from django.shortcuts import render
import json
from math import radians, sin, cos, sqrt, atan2


#  def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    return render(request, "map/example.html")

def save_location(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            # Process or save the location data as needed
            print(f"Received location: Latitude {latitude}, Longitude {longitude}")

            return JsonResponse({'message': 'Location received successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    R = 6371.0  # Radius of the Earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance