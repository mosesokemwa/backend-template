import json

from config import __version__
from django.contrib.auth.tokens import default_token_generator
from django.test import RequestFactory
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import UserModel


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class AuthenticationTests(APITestCase):

    def setUp(self) -> None:
        #  Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = UserModel.objects.create(
            email='user_factoru@test.com',
            password='top_secret_factory',
            first_name='admin_user_factory'
        )
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + get_tokens_for_user(self.user)['access'])



    def test_register_view(self):
        """
        Ensure we can create a new account object.
        """
        data = {'email':'user@test.com', 'password':'top_secret', 'password2':'top_secret', 'first_name':'admin_user'}
        response = self.client.post('/api/register/', data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_view(self):
        # login data
        data = {'email':'user@test.com', 'password':'top_secret'}
        # Create an instance of a GET request.
        response = self.client.get('/api/login/', data)
        # Test that the response is 200 OK.
        self.assertEqual(response.data['access'], get_tokens_for_user(self.user)['access'])
        self.assertEqual(response.data['refresh'], get_tokens_for_user(self.user)['refresh'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_profile_view(self):
        # Create an instance of a GET request.
        data = {
            'first_name':'admin_user_first',
            'last_name':'admin_user_last',
            'middle_name':'admin_user_middle',
            'dob': '2020-01-01',
            'phone_number':'1234567890'
            }
        # add access token to request
        response = self.client.patch('/api/update/profile/', data)


        # Test that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Test that the response coincides with the request data.
        # data in request should be part of response data
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertEqual(response.data['middle_name'], data['middle_name'])
        self.assertEqual(response.data['dob'], data['dob'])
        self.assertEqual(response.data['phone_number'], data['phone_number'])

    def test_update_address_view(self):
        data = {
            "nationality": 'Kenyan',
            "country": 'Kenya',
            "state": 'Nairobi',
            "city": 'Nairobi',
            "zip": '00100'
        }
        # Create an instance of a GET request.
        response = self.client.patch('/api/update/address/', data)
        # Test that the response is 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response.data, json.dumps(data))



    def test_user_model(self):
        user_model = UserModel()
        self.assertEqual(user_model.email, 'user@test.com')
        self.assertEqual(user_model.password, 'top_secret')
        self.assertEqual(user_model.first_name, 'admin_user')
        self.assertEqual(user_model.is_active, False)


    def test_private_view(self):
        # Create an instance of a GET request.
        response = self.client.get('/api/private/')
        # Test that the response is 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Hello World!'})


    def test_confirm_email_view(self):
        user = UserModel()
        confirmation_token = default_token_generator.make_token(user)
        # Create an instance of a GET request.
        response = self.client.get(f'/api/confirm-email/?confirmation_token={confirmation_token}')
        # Test that the response is 200 OK.
        self.assertEqual(response.data, {'message': 'Email confirmed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

