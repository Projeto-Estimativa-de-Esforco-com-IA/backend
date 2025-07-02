from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('get_all_teams', views.get_teams, name='get_all_teams'),
]
