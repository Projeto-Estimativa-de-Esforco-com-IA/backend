from django.urls import path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Planning Poker API",
      default_version='v1',
      description="Documentação automática da API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Projects
    path('projects/', views.list_projects, name='list_projects'),
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:project_id>/delete/', views.remove_project, name='remove_project'),

    # Tasks
    path('projects/<int:project_id>/tasks/', views.list_tasks, name='list_tasks'),
    path('projects/<int:project_id>/tasks/add/', views.add_task, name='add_task'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:task_id>/delete/', views.remove_task, name='remove_task'),

    # Planning Sessions
    path('planning-sessions/start/', views.start_session, name='start_session'),
    path('planning-sessions/<int:session_id>/delete/', views.remove_session, name='remove_session'),

    # Votes
    path('planning-sessions/vote/', views.vote_task, name='vote_task'),

    # Estimate
    path('planning-sessions/finalize/', views.finalize_task_estimate, name='finalize_task_estimate'),
        path('users/', views.list_users, name='list_users'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),

]
