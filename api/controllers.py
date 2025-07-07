from django.db import transaction
from django.utils import timezone
from .models import Project, Task, PlanningSession, Vote, TaskEstimate


def create_project(data):
    project = Project.objects.create(
        name=data['name'],
        description=data.get('description', ''),
        category=data.get('category')
    )
    return project


def update_project(project, data):
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)
    project.category = data.get('category', project.category)
    project.save()
    return project


def delete_project(project):
    project.delete()


def create_task(project_id, data):
    project = Project.objects.get(id=project_id)
    task = Task.objects.create(
        project=project,
        title=data['title'],
        description=data.get('description', ''),
        category=data.get('category')
    )
    return task


def update_task(task, data):
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.category = data.get('category', task.category)
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
