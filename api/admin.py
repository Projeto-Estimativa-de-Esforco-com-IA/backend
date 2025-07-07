from django.contrib import admin
from .models import Project, Team, Category, TeamMembership
# Register your models here.

admin.site.register(Team)
admin.site.register(Project)
admin.site.register(Category)
admin.site.register(TeamMembership)