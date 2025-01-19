from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # For rendering the example.html
    path('save-location/', views.save_location, name='save_location'),  # For receiving location data
]

