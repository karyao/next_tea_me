from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('', views.brew_page, name='brew_page'),
]