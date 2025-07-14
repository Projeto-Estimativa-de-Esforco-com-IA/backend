from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    phone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    department = models.CharField("Departamento", max_length=100, blank=True, null=True)
    is_manager = models.BooleanField("É gerente?", default=False)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        verbose_name="groups",
        help_text="The groups this user belongs to."
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        blank=True,
        verbose_name="user permissions",
        help_text="Specific permissions for this user."
    )

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    """
    Projeto principal contendo iniciativas do Gerente de Projeto.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Tarefas associadas a um projeto, conforme backlog.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.name} - {self.title}"


class Team(models.Model):
    """
    Equipe responsável pelas estimativas e execução de tarefas.
    """
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='TeamMembership', related_name='teams')

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    """
    Associação de usuários a equipes.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'team')


class PlanningSession(models.Model):
    """
    Sessão de Planning Poker vinculada a um projeto e um conjunto de tarefas.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='planning_sessions')
    tasks = models.ManyToManyField(Task, related_name='planning_sessions')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='planning_sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Planning #{self.id} - {self.project.name}"


class Vote(models.Model):
    """
    Voto de estimativa de um membro durante o Planning Poker.
    Valores típicos da sequência Fibonacci: 0, 1, 2, 3, 5, 8, 13, 21, ?
    """
    session = models.ForeignKey(PlanningSession, on_delete=models.CASCADE, related_name='votes')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.CharField(max_length=10)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'task', 'user')


class TaskEstimate(models.Model):
    """
    Histórico de estimativas finais de uma tarefa após sessão de Planning Poker.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='estimates')
    session = models.ForeignKey(PlanningSession, on_delete=models.CASCADE, related_name='task_estimates')
    average = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Estimate {self.average} for {self.task.title}"


class Prediction(models.Model):
    """
    Sugestão de esforço gerada pelo modelo de IA antes do Planning Poker.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='predictions')
    suggested_effort = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction {self.suggested_effort} for {self.project.name}"


# Optional: Registro de usuários extras caso precise de campos além do AUTH_USER_MODEL
# from django.contrib.auth.models import AbstractUser
# class User(AbstractUser):
#     pass
