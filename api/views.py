from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .controllers import (
    create_project, update_project, delete_project,
    create_task, update_task, delete_task,
    start_planning_session, submit_vote, finalize_estimate,
    delete_session
)
from .models import Project, Task, PlanningSession
from .serializers import (
    ProjectSerializer, TaskSerializer, PlanningSessionSerializer,
    TaskEstimateSerializer, UserSerializer
)
from django.contrib.auth.models import User

# ---- PROJECTS ----

@swagger_auto_schema(method='post', request_body=ProjectSerializer)
@api_view(['POST'])
def add_project(request):
    project = create_project(request.data)
    serializer = ProjectSerializer(project)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def list_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@swagger_auto_schema(methods=['put', 'patch'], request_body=ProjectSerializer)
@api_view(['PUT', 'PATCH'])
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    updated = update_project(project, request.data)
    serializer = ProjectSerializer(updated)
    return Response(serializer.data)


@api_view(['DELETE'])
def remove_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    delete_project(project)
    return Response(status=status.HTTP_204_NO_CONTENT)


# ---- TASKS ----

@swagger_auto_schema(method='post', request_body=TaskSerializer)
@api_view(['POST'])
def add_task(request, project_id):
    task = create_task(project_id, request.data)
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def list_tasks(request, project_id):
    tasks = Task.objects.filter(project_id=project_id)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@swagger_auto_schema(methods=['put', 'patch'], request_body=TaskSerializer)
@api_view(['PUT', 'PATCH'])
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    updated = update_task(task, request.data)
    serializer = TaskSerializer(updated)
    return Response(serializer.data)


@api_view(['DELETE'])
def remove_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    delete_task(task)
    return Response(status=status.HTTP_204_NO_CONTENT)


# ---- PLANNING SESSION ----

@swagger_auto_schema(method='post', request_body=PlanningSessionSerializer)
@api_view(['POST'])
def start_session(request):
    project_id = request.data['project_id']
    team_id = request.data['team_id']
    task_ids = request.data['task_ids']

    session = start_planning_session(project_id, team_id, task_ids)
    serializer = PlanningSessionSerializer(session)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def remove_session(request, session_id):
    session = get_object_or_404(PlanningSession, id=session_id)
    delete_session(session)
    return Response(status=status.HTTP_204_NO_CONTENT)


# ---- VOTES ----

from rest_framework import serializers
from drf_yasg import openapi

class VoteRequestSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    task_id = serializers.IntegerField()
    value = serializers.IntegerField()


@swagger_auto_schema(method='post', request_body=VoteRequestSerializer)
@api_view(['POST'])
def vote_task(request):
    session_id = request.data['session_id']
    task_id = request.data['task_id']
    value = request.data['value']

    vote = submit_vote(session_id, task_id, request.user, value)
    return Response({"detail": "Voto registrado com sucesso."}, status=status.HTTP_201_CREATED)


# ---- ESTIMATE ----

class FinalizeEstimateRequestSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    task_id = serializers.IntegerField()

@swagger_auto_schema(method='post', request_body=FinalizeEstimateRequestSerializer)
@api_view(['POST'])
def finalize_task_estimate(request):
    session_id = request.data['session_id']
    task_id = request.data['task_id']

    estimate = finalize_estimate(session_id, task_id)
    serializer = TaskEstimateSerializer(estimate)
    return Response(serializer.data)


# ---- USERS ----

@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['POST'])
def add_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['put', 'patch'], request_body=UserSerializer)
@api_view(['PUT', 'PATCH'])
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
