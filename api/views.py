from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Team, Project
from .serializers import ProjectSerializer, TeamSerializer

import json

@api_view(['GET'])
def get_teams(request):
    
    if request.method == 'GET':
        teams = Team.objects.all()
        
        serializer = TeamSerializer(teams, many=True)
        
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)