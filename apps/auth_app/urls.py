from django.urls import path
from knox.views import LogoutAllView, LogoutView

from apps.auth_app.views import LoginView, UserViewSet

urlpatterns = [
    path('user/login', LoginView.as_view(), name='auth_user_login_create'),
    path('user/logout', LogoutView.as_view(), name='auth_user_logout_create'),
    path('user/logout/all', LogoutAllView.as_view(), name='auth_user_logout_all_create'),
    path('users', UserViewSet.as_view({'get': 'list'}), name='auth_users_list'),
    path('users/<int:pk>', UserViewSet.as_view(
        {'patch': 'partial_update', 'get': 'retrieve', 'put': 'update',
         'delete': 'partial_destroy'}), name='auth_users_cms'),
]
