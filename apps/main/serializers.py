from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.main.models import ResidentialAddressModel


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['id'] = user.id
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ('password', 'password2', 'email', 'first_name',)
        extra_kwargs = {
            'first_name': {'required': True},
            'email': {'required': True},
            'password': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            password=validated_data['password']
        )

        user.set_password(validated_data['password'])

        # generate token
        confirmation_token = default_token_generator.make_token(user)
        user.email_verification_token = confirmation_token
        user.save()

        # send email
        activation_link = (f"{settings.FRONTEND_URL}/confirm-email/?user_id={user.id}"
                           f"&confirmation_token={confirmation_token}")

        send_mail(
            'Email Confirmation',
            f'Email confirmation link: {activation_link}',
            settings.DEFAULT_FROM_EMAIL,
            [validated_data['email']],
            fail_silently=False,
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    email = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', "middle_name", "last_name", "dob", "phone_number", ]
        depth = 2


class ResidentialAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentialAddressModel
        fields = ['id', "nationality", "country", "state", "city", "zip", ]
