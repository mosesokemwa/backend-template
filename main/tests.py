from config import __version__
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase


from main.models import UserModel, UserManager
from main.views import ConfirmEmailView, ResidentialAddressView, LoginView, PrivateView, RegisterView, UpdateProfileView

class AuthenticationTest(TestCase):
    def setUp(self) -> None:
        #  Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = UserModel.objects.create(email='user@test.com', password='top_secret', first_name='admin_user')

    def test_login_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('/api/login/')
        request.user = AnonymousUser()
        # Test that the response is 200 OK.
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('/api/register/')
        request.user = AnonymousUser()
        # Test that the response is 200 OK.
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_confirm_email_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('/api/confirm-email/')
        request.user = self.user
        # Test that the response is 200 OK.
        response = ConfirmEmailView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_update_profile_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('/api/update/profile/')
        request.user = self.user
        # Test that the response is 200 OK.
        response = UpdateProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_update_address_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('/api/update/address/')
        request.user = self.user
        # Test that the response is 200 OK.
        response = ResidentialAddressView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_private_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('/api/private/')
        request.user = self.user
        # Test that the response is 200 OK.
        response = PrivateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_model(self):
        user_model = UserModel()
        self.assertEqual(user_model.email, 'user@test.com')
        self.assertEqual(user_model.password, 'top_secret')
        self.assertEqual(user_model.first_name, 'admin_user')
        self.assertEqual(user_model.is_active, False)

    def test_version(self):
            self.assertEqual(__version__, '0.1.0')
