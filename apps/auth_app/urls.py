from django.urls import path
from knox.views import LogoutAllView, LogoutView

from apps.auth_app.views import LoginView

urlpatterns = [
    path('user/login', LoginView.as_view(), name='sign_in'),
    path('user/logout', LogoutView.as_view(), name='sign_out'),
    path('user/logout/all', LogoutAllView.as_view(), name='sign_out_all'),
]
