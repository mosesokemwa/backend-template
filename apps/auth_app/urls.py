from django.urls import path
from knox.views import LogoutAllView, LogoutView
from rest_framework.routers import DefaultRouter

from apps.auth_app.views import LoginView, UserViewSet

router = DefaultRouter()

urlpatterns = [
    path('user/login', LoginView.as_view(), name='sign_in'),
    path('user/logout', LogoutView.as_view(), name='sign_out'),
    path('user/logout/all', LogoutAllView.as_view(), name='sign_out_all'),
]

router.register(r'users', UserViewSet, basename='user_cms')

urlpatterns += router.urls
