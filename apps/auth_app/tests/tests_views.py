from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class TestLoginViewPost(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.api_client = APIClient()

    def test_login_view_post(self):
        # Arrange
        url = reverse('login')
        username = 'testuser'
        password = '12345'
        status_code = status.HTTP_200_OK

        # Act
        response = self.api_client.post(url, data={'username': username, 'password': password})

        # Assert
        self.assertEqual(response.status_code, status_code)
        if status_code != status.HTTP_200_OK:
            return
        self.assertIn('token', response.data)

    def test_login_view_post_wrong_password(self):
        # Arrange
        url = reverse('login')
        username = 'testuser'
        password = 'wrongpassword'
        status_code = status.HTTP_400_BAD_REQUEST

        # Act
        response = self.api_client.post(url, data={'username': username, 'password': password})

        # Assert
        self.assertEqual(response.status_code, status_code)
