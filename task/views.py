from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Membership, Task, Team
from .serializers import MembershipSerializer, TaskSerializer, TeamSerializer


@api_view(['GET'])
def task_list(request):
    if request.user.is_superuser:
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    # tasks = Task.objects.filter(by=request.user)
    tasks = Task.objects.filter(by=request.user) | Task.objects.filter(team__memberships__member=request.user)
    tasks = tasks.distinct()

    if tasks.exists():
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    else:
        tasks = []
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if task.by != request.user:
        return Response({'error': 'Unauthorized.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = TaskSerializer(task)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    user=request._request.user

    if serializer.is_valid():
        serializer.validated_data['by'] = user
        serializer.validated_data['username'] = user.username
        serializer.save()
        if 'team' in serializer.validated_data:
            try:
                team = Team.objects.get(teamname=serializer.validated_data['team'])
                memberships = Membership.objects.filter(team=team)
                for membership in memberships:
                    member_email = membership.member.email
                    try:
                        send_mail(
                            f'A new task by {user.username} has been assigned',             #subject
                            f'''A new task by {user.username} has been assigned
                                "{serializer.validated_data['content']}"
                            ''',                                                                                    #message
                            settings.EMAIL_HOST_USER,                                                               #sender
                            [f'{member_email}'],                                                                    #receiver
                            fail_silently=False
                            )
                    except Exception as e:
                        extra_messages = {'error': 'There has been an error notifying other members'}
            except Team.DoesNotExist:
                extra_messages = {'error': 'Team not found'}
        else:
            extra_messages = {'error': 'No team was selected'}
        return Response({'data':serializer.data, 'extra_messages': extra_messages}, status=status.HTTP_201_CREATED)
    print(serializer.errors, serializer)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user.is_superuser:
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
    # if task.by != request.user:
    if task.by != request.user and not task.team.memberships.filter(member=request.user).exists():
        return Response({'error': 'Unauthorized.'}, status=status.HTTP_403_FORBIDDEN)

    if task.by == request.user or task.team.memberships.filter(member=request.user).exists():
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            # print(serializer)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user.is_superuser:
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if task.by != request.user and not task.team.memberships.filter(member=request.user).exists(): #.user
        return Response({'error': 'Unauthorized.'}, status=status.HTTP_403_FORBIDDEN)

    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)













# teams

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teams(request):
    if request.user.is_superuser:
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    memberships = Membership.objects.filter(member=request.user)
    teams = []
    for membership in memberships:
        teams.append(membership.team)
    
    if not teams:
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_team(request):
    teamserializer = TeamSerializer(data=request.data)
    if teamserializer.is_valid():
        teamserializer.save()

        this_new_team = Team.objects.get(teamname=teamserializer.validated_data['teamname'])
        membership = Membership(team=this_new_team, member=request.user)
        membership.save()

        return Response(teamserializer.data, status=status.HTTP_201_CREATED)
    return Response(teamserializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_team(request, id):
    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TeamSerializer(team)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_team(request, id):
    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TeamSerializer(team, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_team(request, id):
    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    team.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_to_team(request):
    teamId = request.data.get('teamId')
    userId = request.data.get('userId')

    print(teamId, userId)
    
    team = Team.objects.get(id=teamId)
    print(team)

    user = User.objects.get(id=userId)
    print(user)
    
    membership = Membership(team=team, member=user)
    membership.save()

    return Response({'membership':'membership created'}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def leave_team(request, id):
    team = Team.objects.get(id=id)
    membership = Membership.objects.get(team=team, member=request.user)
    membership.delete()
    return Response({'message': 'Membership to team was cancelled.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def teamTasks(request):
    teamId = request.data.get('teamId')
    try:
        team = Team.objects.get(id=teamId)
        tasks = team.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Team.DoesNotExist:
        return Response({'message':'Team not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teammates(request, id):
    try:
        teammates = []
        team = Team.objects.get(id=id)
        for m in team.memberships.all():
            teammates.append(m.member.username)
        return Response(teammates, status=status.HTTP_200_OK)
    except Team.DoesNotExist:
        return Response([], status=status.HTTP_200_OK)
    # try:
    #     memberships = Membership.objects.filter(team=id)
    #     member_names = [membership.member.username for membership in memberships]
    #     return Response(member_names, status=status.HTTP_200_OK)
    # except Membership.DoesNotExist:
    #     return Response([], status=status.HTTP_200_OK)
        




# base view

def frontpage(request):
    if request.user.is_authenticated:
       return render(request, 'all-tasks.html')
    return redirect('loginpage')
