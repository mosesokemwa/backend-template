from typing import List

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from main.models import ResidentialAddressModel

from main.serializers import (MyTokenObtainPairSerializer, RegisterSerializer, ResidentialAddressSerializer,
                              UserSerializer)


class RegisterView(CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    http_method_names: List[str] = ['post']

    def perform_create(self, serializer):
        serializer.save()

class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    http_method_names: List[str] = ['post']


class PrivateView(APIView):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names: List[str] = ['get',]

    def get(self, request):
        return Response({'message': 'Hello World!'})

class ResidentialAddressView(UpdateAPIView):
    queryset = ResidentialAddressModel.objects.all()
    serializer_class = ResidentialAddressSerializer
    permission_classes = [IsAuthenticated]
    http_method_names: List[str] = ['get', 'put', 'patch']

    def get_object(self):
        return self.request.user

    def get_queryset(self, pk):
        return self.queryset.filter(id=pk)

class UpdateProfileView(UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names: List[str] = ['get', 'put', 'patch']

    def get_object(self):
        return self.request.user

    def get_queryset(self, pk):
        return self.queryset.filter(id=pk)


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']
    queryset = get_user_model().objects.all()

    def get(self, request):
        user_id = request.query_params.get('user_id', '')
        confirmation_token = request.query_params.get('confirmation_token', '')

        if not user_id or not confirmation_token:
            return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        # user model instance
        user = get_user_model().objects.get(id=user_id)
        if not default_token_generator.check_token(user, confirmation_token):
                return Response('Token is invalid or expired. Please request another confirmation email by signing in.', status=status.HTTP_400_BAD_REQUEST)

        if user.email_verified:
            return True
        if user.email_verification_token == confirmation_token:
            user.email_verified = True
            user.email_verification_token = None
            user.is_active = True
            user.save()
            return Response({'message': 'Email confirmed'})

