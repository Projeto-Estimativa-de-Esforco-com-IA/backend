from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .controllers import (
    create_project, update_project, delete_project,
    create_task, update_task, delete_task,
    start_planning_session, submit_vote, finalize_estimate,
    delete_session
)
from .models import Project, Task, PlanningSession
from .serializers import ProjectSerializer, TaskSerializer, PlanningSessionSerializer, TaskEstimateSerializer


# ---- PROJECTS ----

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

@api_view(['POST'])
def vote_task(request):
    session_id = request.data['session_id']
    task_id = request.data['task_id']
    value = request.data['value']

    vote = submit_vote(session_id, task_id, request.user, value)
    return Response({"detail": "Voto registrado com sucesso."}, status=status.HTTP_201_CREATED)


# ---- ESTIMATE ----

@api_view(['POST'])
def finalize_task_estimate(request):
    session_id = request.data['session_id']
    task_id = request.data['task_id']

    estimate = finalize_estimate(session_id, task_id)
    serializer = TaskEstimateSerializer(estimate)
    return Response(serializer.data)
