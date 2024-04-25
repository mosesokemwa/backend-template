from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from apps.auth_app.models import User
from apps.auth_app.serializers import AuthTokenSerializer, UserSerializer


# Create your views here.
class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    throttle_classes = (UserRateThrottle,)
    serializer_class = AuthTokenSerializer

    @swagger_auto_schema(
        request_body=AuthTokenSerializer,
        responses={200: openapi.Response('Success', AuthTokenSerializer),
                   400: 'Bad Request'},
    )
    # @csrf_exempt
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    filter_fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'staff', 'admin']
    search_fields = ['id', 'email', 'first_name', 'last_name']
    ordering_fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'staff', 'admin']

    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        if self.request.user.admin:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_destroy(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.is_deleted = True
        user.save()
        return Response(status=204)
