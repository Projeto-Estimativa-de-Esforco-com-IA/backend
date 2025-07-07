# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Category
    path('categories/', views.category_list, name='category_list'),

    # Project
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),

    # Task
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),

    # Planning Session
    path('planningsessions/', views.planning_list, name='planning_list'),

    # Vote
    path('votes/', views.vote_list, name='vote_list'),

    # Estimate
    path('estimates/', views.estimate_list, name='estimate_list'),

    # Prediction
    path('predictions/', views.prediction_list, name='prediction_list'),

    # Team
    path('teams/', views.team_list, name='team_list'),
    path('teams/<int:pk>/', views.team_detail, name='team_detail'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
]
