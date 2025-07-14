# serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Project, Task, PlanningSession, Vote, TaskEstimate, Prediction, Category, Team, TeamMembership
)

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'category', 'name', 'description', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class PlanningSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanningSession
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class TaskEstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskEstimate
        fields = '__all__'


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'


# ---------- TEAM com membros detalhados ----------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TeamMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TeamMembership
        fields = ['user', 'joined_at']


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, write_only=True)
    memberships = TeamMembershipSerializer(source='teammembership_set', many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'members', 'memberships']

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        team = Team.objects.create(**validated_data)
        for user in members:
            TeamMembership.objects.create(user=user, team=team)
        return team

    def update(self, instance, validated_data):
        members = validated_data.pop('members', None)
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        if members is not None:
            TeamMembership.objects.filter(team=instance).delete()
            for user in members:
                TeamMembership.objects.create(user=user, team=instance)

        return instance


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        
    def validate_email(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("O campo de email não pode ser vazio.")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance