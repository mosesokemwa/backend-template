from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from apps.main.models import UserModel


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'password')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'password')
