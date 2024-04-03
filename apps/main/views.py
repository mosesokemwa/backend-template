import json
from typing import List

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.main.models import ResidentialAddressModel
from apps.main.serializers import (MyTokenObtainPairSerializer,
                                   RegisterSerializer,
                                   ResidentialAddressSerializer,
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


# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)
#     http_method_names: List[str] = ['post']

#     def post(self, request):
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)

class UserView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    http_method_names: List[str] = ['get', 'put', 'patch']

    def get_object(self, request):
        token = request.headers['Authorization'].split(' ')[1]
        return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])['id']

    def get(self, request, format=None):
        token = request.headers['Authorization'].split(' ')[1]
        user_id = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])['id']
        user = get_user_model().objects.get(id=user_id)
        # add residential address using user_id as foreign key
        residential_address = ResidentialAddressModel.objects.get(user_id=user)
        user_json = UserSerializer(user).data
        user_json['residential_address'] = ResidentialAddressSerializer(residential_address).data
        return Response(user_json)

        # serializer = UserSerializer(user, context={'residential_address': residential_address_list_json})
        # print(serializer.data)
        # return Response(serializer.data)

    def put(self, request, format=None):
        user_id = self.get_object(request)
        user = get_user_model().objects.get(id=user_id)
        serializer = UserSerializer(user, data=json.loads(request.body), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrivateView(APIView):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names: List[str] = ['get', ]

    def get(self, request):
        return Response({'message': 'Hello World!'})


class ResidentialAddressView(APIView):
    queryset = ResidentialAddressModel.objects.all()
    serializer_class = ResidentialAddressSerializer
    permission_classes = [IsAuthenticated]
    http_method_names: List[str] = ['get', 'post', 'put', 'patch']

    def get_object(self, request):
        token = request.headers['Authorization'].split(' ')[1]
        return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])['id']

    def get_queryset(self, pk):
        return self.queryset.filter(id=pk)

    def post(self, request):
        user = self.get_object(request)
        data = json.loads(request.body)
        data['user'] = user
        serializer = ResidentialAddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = self.get_object(request)
        residential_address = ResidentialAddressModel.objects.get(user=user)
        serializer = ResidentialAddressSerializer(residential_address)
        return Response(serializer.data)

    def put(self, request):
        user = self.get_object(request)
        residential_address = ResidentialAddressModel.objects.get(user=user)
        serializer = ResidentialAddressSerializer(residential_address,
                                                  data=json.loads(request.body), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return Response(
                'Token is invalid or expired. Please request another confirmation email by signing in.',
                status=status.HTTP_400_BAD_REQUEST)

        if user.email_verified:
            return True
        if user.email_verification_token == confirmation_token:
            user.email_verified = True
            user.email_verification_token = None
            user.is_active = True
            user.save()
            return Response({'message': 'Email confirmed'})
