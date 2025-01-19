from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Friendship, Message
from django.db.models import Q

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login

from django.http import JsonResponse

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
    
    friends = Friendship.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    )
    return render(request, 'core/index.html', {'friends': friends})

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
    return redirect('index')

@login_required
def add_friend(request, username):
    friend = get_object_or_404(User, username=username)
    if friend != request.user:
        Friendship.objects.get_or_create(
            user1=request.user,
            user2=friend
        )
    return redirect('index')

def brew_page(request):
    return render(request, 'core/brew_page.html')

def brewing_view(request):
    return render(request, 'core/brewing.html')

# Simulate an active socket connection
active_connections = 1  # Assume 1 active connection for demo purposes

def check_for_socket(request):
    # Check if there's an active connection or if we need to create a new one
    if active_connections == 1:
        # If one connection is already active, another user can join
        return JsonResponse({'socket_available': True})
    else:
        # If no connection or pairings, create a new socket connection
        return JsonResponse({'socket_available': False})