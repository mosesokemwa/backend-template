from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


# class AuthTokenSerializer(serializers.Serializer):
#     email = serializers.EmailField(
#         label=_("Email"),
#         write_only=True
#     )
#     password = serializers.CharField(
#         label=_("Password"),
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#         write_only=True
#     )
#
#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#
#         user_obj = User.objects.filter(email=email).first()
#         if user_obj is not None:
#             credentials = {
#                 'email': email,
#                 'password': password
#             }
#
#             print(credentials)
#
#             if all(credentials.values()):
#                 user = authenticate(request=self.context.get('request'), **credentials)
#
#                 if not user:
#                     msg = _('Unable to log in with provided credentials.')
#                     raise serializers.ValidationError(msg, code='authorization')
#             else:
#                 msg = _('Must include "email" and "password".')
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = _('Account with this email/username does not exists')
#             raise serializers.ValidationError(msg, code='authorization')
#
#         attrs['user'] = user
#         return attrs


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
        self.validate_password_last_updated(user_obj)
        self.validate_email_verified(user_obj)
        attrs = self.validate_user_details(user_obj, credentials, attrs)
        return attrs

    @staticmethod
    def validate_password_last_updated(user_obj):
        """Check if user needs to change password
        formulae: today - password_last_updated > 90 days
        """
        if user_obj.password_last_updated:
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
        fields = ['id', 'first_name', 'last_name', 'email', 'is_active', 'staff', 'admin']
        read_only_fields = ['id', 'is_active', 'staff', 'admin']
        extra_kwargs = {
            'password': {'write_only': True}
        }
