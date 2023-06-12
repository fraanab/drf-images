from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from task.models import Membership, Team
from task.serializers import MembershipSerializer, TeamSerializer

from .serializers import AllUsersSerializer, LoginSerializer, UserSerializer


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': 'User created, you can log in'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        return Response({'success': 'Login successful', 'user_data': user_data}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'success': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUsers(request):
    users = User.objects.all()
    serializer = AllUsersSerializer(users, many=True)
    return Response({'users': serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getUser(request):
    username = request.data.get('username')
    user = User.objects.filter(username__contains=username)
    authserializer = AllUsersSerializer(user, many=True)

    memberships = []
    for u in user:
        if Membership.objects.filter(member=request.user):
            for m in Membership.objects.filter(member=request.user):
                memberships.append(m)
                membershipsSerializer = MembershipSerializer(memberships, many=True)
                return Response({
                    'memberships': membershipsSerializer.data, 
                    'users': authserializer.data}, 
                    status=status.HTTP_200_OK
                    )
        else:
            return Response({
                'memberships': 'User is not a member of any teams', 
                'users': authserializer.data}, 
                status=status.HTTP_200_OK
                )
    # return Response(authserializer.data)


# login page

def login_page(request):
    return render(request, 'login.html')

def signup_page(request):
    return render(request, 'signup.html')
