from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        credentials = {
            'email': email,
            'password': password
        }

        user_obj = User.objects.filter(email=email).first()
        # validate user details
        attrs = self.validate_user_details(user_obj, credentials, attrs)
        if user_obj is not None:
            self.validate_password_last_updated(user_obj)
            self.validate_email_verified(user_obj)
        return attrs

    @staticmethod
    def validate_password_last_updated(user_obj):
        """Check if user needs to change password
        formulae: today - password_last_updated > 90 days
        """
        if user_obj.password_last_updated:
            days = (timezone.now() - user_obj.password_last_updated).days
            if days > 90:
                msg = _("Your password has not been updated for more than 90 days. Please update "
                        "your password.")
                raise serializers.ValidationError(msg, code='authorization')

    @staticmethod
    def validate_email_verified(user_obj):
        if not user_obj.email_verified:
            msg = _('Email is not verified')
            raise serializers.ValidationError(msg, code='authorization')

    def validate_user_details(self, user_obj, credentials, attrs):
        if user_obj is not None:

            if all(credentials.values()):
                user = authenticate(request=self.context.get('request'), **credentials)

                if not user:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = _('Must include "email" and "password".')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Account with this email/username does not exists')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        read_only_fields = ('is_active', 'is_staff', 'is_superuser')

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                _("Password must be at least 8 characters long.")
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                _("User with this email already exists.")
            )
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                _("User with this username already exists.")
            )
        return value

    def validate(self, data):
        if data.get('email'):
            self.validate_email(data['email'])
        if data.get('password'):
            self.validate_password(data['password'])
        if data.get('username'):
            self.validate_username(data['username'])
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
