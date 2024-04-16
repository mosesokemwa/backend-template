from django.contrib.auth import login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, viewsets
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


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    filter_fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'staff', 'admin']
    search_fields = ['id', 'email', 'first_name', 'last_name']
    ordering_fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'staff', 'admin']

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        if self.request.user.admin:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
