from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Friendship, Message
from django.db.models import Q

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login

from django.http import HttpResponseServerError
from django.http import JsonResponse
import json
from math import radians, sin, cos, sqrt, atan2

def index(request):
    if not request.user.is_authenticated:
        # Create test users if they don't exist
        if not User.objects.filter(username='user1').exists():
            User.objects.create_user('user1')
        if not User.objects.filter(username='user2').exists():
            User.objects.create_user('user2')
        
        # Create friendship between test users
        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')
        Friendship.objects.get_or_create(user1=user1, user2=user2)
        
        # Auto-login as user1 for testing
        from django.contrib.auth import login
        login(request, user1)

    # Fetch friends related to the logged-in user
    friends = Friendship.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    )
    
    # Pass the username of the logged-in user to the template
    return render(request, 'core/index.html', {'friends': friends, 'username': request.user.username})


def chat_room(request, username):
    friend = User.objects.get(username=username)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=friend)) |
        (Q(sender=friend) & Q(receiver=request.user))
    ).order_by('timestamp')
    return render(request, 'core/chat_room.html', {
        'friend': friend,
        'messages': messages
    })

def test_login(request):
    test_users = User.objects.filter(username__in=['user1', 'user2'])
    return render(request, 'core/test_login.html', {'users': test_users})

def switch_user(request, username):
    user = User.objects.get(username=username)
    login(request, user)
    return redirect('/')

# def add_friend(request, username):
#     friend = get_object_or_404(User, username=username)
#     if friend != request.user:
#         Friendship.objects.get_or_create(
#             user1=request.user,
#             user2=friend
#         )
#     return redirect('index')

@login_required
def add_friend(request):
    try:
        partner_name = request.GET.get('partner', None)
        print(f"Received partner: {partner_name}")  # Debugging line
        
        if not partner_name:
            return HttpResponseServerError("Partner name is missing.")
        
        # Check if the partner exists in the database
        if not User.objects.filter(username=partner_name).exists():
            return HttpResponseServerError(f"No user found with the username {partner_name}.")

        # Fetch the partner from the database
        partner = get_object_or_404(User, username=partner_name)

        # Check if the users are already friends
        existing_friendship = Friendship.objects.filter(
            (Q(user1=request.user) & Q(user2=partner)) | (Q(user1=partner) & Q(user2=request.user))
        ).exists()

        if existing_friendship:
            return render(request, 'core/add_friend.html', {'partner': partner, 'already_friends': True})

        # If not friends, create the friendship
        Friendship.objects.create(user1=request.user, user2=partner)

        return render(request, 'core/add_friend.html', {'partner': partner, 'already_friends': False})

    except Exception as e:
        return HttpResponseServerError(f"An error occurred: {str(e)}")


def brew_page(request):
    return render(request, 'core/brew_page.html')

def brewing_view(request):
    return render(request, 'core/brewing.html')

def example_map(request):
    return render(request, "core/example.html")

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
