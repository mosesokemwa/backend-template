import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.test import APIClient


class TestAuthViews:

    @pytest.fixture
    def user(self, db):
        return User.objects.create_user(username='testuser', password='12345')

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.mark.django_db
    @pytest.mark.parametrize("username, password, status_code", [
        # Happy path tests
        ('testuser', '12345', status.HTTP_200_OK),

        # Error cases
        ('testuser', 'wrongpassword', status.HTTP_400_BAD_REQUEST),
        ('nonexistentuser', '12345', status.HTTP_400_BAD_REQUEST),
    ])
    def test_login_view_post(self, username, password, status_code, user, api_client):
        url = reverse('login')  # Assuming the URL name for the login view is 'login'

        # Act
        response = api_client.post(url, data={'username': username, 'password': password})

        # Assert
        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            assert 'token' in response.data  # Assuming successful login returns a token

    @pytest.mark.django_db
    def test_logout_view_post(self, user, api_client):
        url = reverse('logout')  # Assuming the URL name for the logout view is 'logout'
        api_client.force_authenticate(user=user)

        # Act
        response = api_client.post(url)

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not get_redis_connection().get(user.auth_token)  # Assuming the auth token is stored in Redis

    @pytest.mark.django_db
    def test_logout_view_post_unauthenticated(self, api_client):
        url = reverse('logout')  # Assuming the URL name for the logout view is 'logout'

        # Act
        response = api_client.post(url)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_logout_view_post_invalid_token(self, user, api_client):
        url = reverse('logout')  # Assuming the URL name for the logout view is 'logout'
        api_client.force_authenticate(user=user)
        user.auth_token.delete()  # Assuming the auth token is deleted

        # Act
        response = api_client.post(url)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # delete redis cache
    @pytest.fixture
    def delete_redis_cache(self):
        get_redis_connection().flushall()
