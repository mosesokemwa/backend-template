from django.urls import path

from apps.main.views import (ConfirmEmailView, LoginView, PrivateView,
                             RegisterView, ResidentialAddressView, UserView)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('user/', UserView.as_view(), name='auth_user'),
    path('address/update', ResidentialAddressView.as_view(), name='auth_update_address'),
    path('confirm/email/', ConfirmEmailView.as_view(), name='auth_confirm_email'),
    path('auth/private/', PrivateView.as_view(), name='auth_private'),
]
