from django.db import transaction
from django.utils import timezone
from .models import Project, Task, PlanningSession, Vote, TaskEstimate, Category
from django.contrib.auth.models import User
from rest_framework import status

def create_project(data):
    category_id = data.get('category')  # Exemplo: 3

    # Buscar a instância de Category com esse ID
    try:
        category_instance = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return status.HTTP_400_BAD_REQUEST
    
    if data["name"]:
        project = Project.objects.create(
            name=data['name'],
            description=data.get('description', ''),
            category=category_instance
        )
        return project
    return status.HTTP_400_BAD_REQUEST


def update_project(project, data):
    category_id = data.get('category')  # Exemplo: 3

    # Buscar a instância de Category com esse ID
    try:
        category_instance = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return status.HTTP_400_BAD_REQUEST
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)
    project.category = category_instance
    project.save()
    return project


def delete_project(project):
    project.delete()


def create_task(project_id, data):
    category_id = data.get('category')  # Exemplo: 3

    # Buscar a instância de Category com esse ID
    try:
        category_instance = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return status.HTTP_400_BAD_REQUEST
    project = Project.objects.get(id=project_id)
    task = Task.objects.create(
        project=project,
        title=data['title'],
        description=data.get('description', ''),
        category=category_instance
    )
    return task


def update_task(task, data):
    category_id = data.get('category')  # Exemplo: 3

    # Buscar a instância de Category com esse ID
    try:
        category_instance = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return status.HTTP_400_BAD_REQUEST
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.category = category_instance
    task.save()
    return task


def delete_task(task):
    task.delete()


def start_planning_session(project_id, team_id, task_ids):
    project = Project.objects.get(id=project_id)
    session = PlanningSession.objects.create(project=project, team_id=team_id)
    session.tasks.set(task_ids)
    session.save()
    return session


def submit_vote(session_id, task_id, user, value):
    session = PlanningSession.objects.get(id=session_id)
    task = Task.objects.get(id=task_id)
    vote = Vote.objects.create(
        session=session,
        task=task,
        user=user,
        value=value
    )
    return vote


@transaction.atomic
def finalize_estimate(session_id, task_id):
    session = PlanningSession.objects.get(id=session_id)
    task = Task.objects.get(id=task_id)
    votes = Vote.objects.filter(session=session, task=task)

    valid_votes = [float(v.value) for v in votes if v.value.isdigit() or v.value.replace('.', '', 1).isdigit()]
    if not valid_votes:
        raise ValueError("Não há votos válidos para calcular a média.")

    avg = sum(valid_votes) / len(valid_votes)

    estimate = TaskEstimate.objects.create(
        task=task,
        session=session,
        average=avg,
        recorded_at=timezone.now()
    )

    session.ended_at = timezone.now()
    session.save()

    return estimate


def delete_session(session):
    session.delete()
