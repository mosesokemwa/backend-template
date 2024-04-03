from django.contrib.auth import login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.throttling import UserRateThrottle

from apps.auth_app.serializers import AuthTokenSerializer


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
