import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


# Assuming pytest is installed and set up for Django
# Fixture for creating a user in the database
@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='12345')


# Fixture for APIClient instance
@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
@pytest.mark.parametrize("username, password, status_code", [
    # Happy path tests
    ('testuser', '12345', status.HTTP_200_OK, 'happy-path-valid-credentials'),

    # Error cases
    ('testuser', 'wrongpassword', status.HTTP_400_BAD_REQUEST, 'error-wrong-password'),
    ('nonexistentuser', '12345', status.HTTP_400_BAD_REQUEST, 'error-nonexistent-user'),
], ids=lambda x: x[-1])
def test_login_view_post(username, password, status_code, user, api_client):
    url = reverse('login')  # Assuming the URL name for the login view is 'login'

    # Act
    response = api_client.post(url, data={'username': username, 'password': password})

    # Assert
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert 'token' in response.data  # Assuming successful login returns a token
