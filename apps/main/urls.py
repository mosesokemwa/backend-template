from django.urls import path

from apps.main.views import (ConfirmEmailView, LoginView, PrivateView,
                             RegisterView, ResidentialAddressView, UserView)

app_name = 'main'

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='main_register'),
    path('auth/login/', LoginView.as_view(), name='main_login'),
    path('user/', UserView.as_view(), name='main_user'),
    path('address/update', ResidentialAddressView.as_view(), name='main_update_address'),
    path('confirm/email/', ConfirmEmailView.as_view(), name='main_confirm_email'),
    path('auth/private/', PrivateView.as_view(), name='main_private'),
]
