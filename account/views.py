import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import logout

from .serializers import *


@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                first_name=serializer.data['first_name'],
                username=serializer.data['username'],
                password=serializer.data['password'],
            )
            return Response({'status': 'success', 'data': serializer.data})
        else:
            return Response({'status': 'failed', 'errors': serializer.errors})
    return Response({'status': 'failed', 'errors': serializer.errors})


@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        # Authenticate the user
        user = authenticate(
            username=serializer.data['username'],
            password=serializer.data['password']
        )

        if user is not None:
            # Return a success response
            return Response({
                'status': 'success',
                'user_id': user.id
            })
        else:
            # Return an error response
            return Response({'status': 'failed', 'message': ['Invalid username or password']})
    else:
        return Response({'status': 'failed', 'message': serializer.errors})


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'status': 'success'})


@api_view(['POST'])
def detail_profile_view(request):
    data = json.loads(request.body)
    try:
        user_id = data['user_id']
        user = User.objects.get(id=user_id)
        user_serializer = UserSerializer(user)
        return Response({
            'status': 'success',
            'data': user_serializer.data  
            })
    except:
        print('User tidak ditemukan')
    return Response({
        'status': 'failed',
        'message': 'User tidak ditemukan'
        })
