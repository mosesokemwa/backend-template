from django.contrib.auth import authenticate, get_user_model
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

        user_obj = User.objects.filter(email=email).first()
        if user_obj is not None:
            credentials = {
                'email': email,
                'password': password
            }

            print(credentials)

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
