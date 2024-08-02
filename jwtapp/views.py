from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .serializers import UserSerializer

# Create your views here.
def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def protected_view(request):
    return render(request, 'index.html')

# Registering Process
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'username': user.username,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Logining Process
class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        access_token = request.data.get('access_token')

        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                # Validate the access token
                UntypedToken(access_token)
                # Respond with success
                return Response({"success": True}, status=status.HTTP_200_OK)
            except (InvalidToken, TokenError):
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
