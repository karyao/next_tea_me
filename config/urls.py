"""
URL configuration for next_tea_me project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.brew_page, name='brew_page'),
    path('chat_room/<str:username>/', views.chat_room, name='chat_room'),
    path('test-login/', views.test_login, name='test_login'),
    path('switch-user/<str:username>/', views.switch_user, name='switch_user'),
    #path('add-friend/<str:username>/', views.add_friend, name='add_friend'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('brewing/', views.brewing_view, name='brewing'),
    # path('brew_page/', views.brew_page, name='brew_page'),
    path('messages/', views.index, name='messages'),
    path('map/',views.example_map, name='example'),
    path('map/save-location/', views.save_location, name='save_location')
]
