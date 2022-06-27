from django.urls import path
from main.views import ConfirmEmailView, ResidentialAddressView, LoginView, PrivateView, RegisterView, UserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('user/', UserView.as_view(), name='auth_user'),
    path('update/address/',ResidentialAddressView.as_view(), name='auth_update_address'),
    path('confirm/email/', ConfirmEmailView.as_view(), name='auth_confirm_email'),
    path('private/', PrivateView.as_view(), name='auth_private'),
]
