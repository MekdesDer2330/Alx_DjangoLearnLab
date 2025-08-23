from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserSerializer
from .models import CustomUser

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user. Accepts username, email, password, bio (optional), profile_picture (optional).
    Returns created user data + token.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        data = UserSerializer(user, context={'request': request}).data
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login using either username OR email in the 'username' field.
    Request JSON: { "username": "alice" or "alice@example.com", "password": "..." }
    """
    identifier = request.data.get('username') or request.data.get('email')
    password = request.data.get('password')

    if not identifier or not password:
        return Response({"detail": "Provide username/email and password."}, status=status.HTTP_400_BAD_REQUEST)

    # allow login by email or username
    username_to_auth = None
    if '@' in identifier:
        try:
            user_obj = CustomUser.objects.get(email=identifier)
            username_to_auth = user_obj.username
        except CustomUser.DoesNotExist:
            username_to_auth = None
    else:
        username_to_auth = identifier

    user = authenticate(username=username_to_auth, password=password)
    if not user:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    data = UserSerializer(user, context={'request': request}).data
    data['token'] = token.key
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """
    Get the authenticated user's profile.
    Requires Authorization: Token <token>
    """
    serializer = UserSerializer(request.user, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_profile_view(request, username):
    """
    Public profile by username (read-only).
    """
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, context={'request': request})
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    if request.user == user_to_follow:
        return Response({'error': 'You cannot follow yourself'}, status=400)
    request.user.following.add(user_to_follow)
    return Response({'message': f'You are now following {user_to_follow.username}'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    request.user.following.remove(user_to_unfollow)
    return Response({'message': f'You have unfollowed {user_to_unfollow.username}'})

