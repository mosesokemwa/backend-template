import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from apps.auth_app.models import ServerSideCredentials

User = get_user_model()


@pytest.mark.django_db
class TestModels(TestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.server_side_credentials = baker.make(ServerSideCredentials)

    def test_user_model(self):
        # Arrange
        # sourcery skip: no-conditionals-in-tests
        if self.user.username is None or self.user.email is None:
            with self.assertRaises(ValueError):
                # Act
                User.objects.create_user(
                    username=self.user.username,
                    first_name=self.user.first_name, email=self.user.email,
                    password=self.user.password,
                    is_active=self.user.is_active, is_admin=self.user.admin,
                    is_staff=self.user.is_staff
                )
        else:
            # Act
            user = User.objects.create_user(
                username=self.user.username,
                first_name=self.user.first_name, email=self.user.email,
                password=self.user.password,
                is_active=self.user.is_active,
                is_admin=self.user.admin,
                is_staff=self.user.is_staff
            )

            # Assert
            self.assertEqual(user.username, self.user.username)
            self.assertEqual(user.first_name, self.user.first_name)
            self.assertEqual(user.email, self.user.email)
            self.assertTrue(user.check_password(self.user.password))
            self.assertEqual(user.is_active, self.user.is_active)
            self.assertEqual(user.is_superuser, self.user.admin)
            self.assertEqual(user.is_staff, self.user.is_staff)

    def test_server_side_credentials(self):
        # ID: HappyPath-1
        api_key = "key123"
        api_secret = "secret123"
        expiry = timezone.now() + timezone.timedelta(days=1)
        is_active = True
        user = baker.make(User)

        # Act
        server_side_credentials = ServerSideCredentials.objects.create(
            api_key=api_key, api_secret=api_secret, expiry=expiry, is_active=is_active, user=user
        )

        # Assert
        self.assertEqual(server_side_credentials.api_key, api_key)
        self.assertEqual(server_side_credentials.api_secret, api_secret)
        self.assertEqual(server_side_credentials.expiry, expiry)
