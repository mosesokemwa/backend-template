import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.auth_app.models import ServerSideCredentials

User = get_user_model()


# Note: The following tests assume the existence of a utils.misc.exclude_by_keys function,
# which is not provided in the code snippet. Adjustments may be needed based on its implementation.

@pytest.mark.django_db
@pytest.mark.parametrize("username,first_name,email,password,is_active,is_admin,is_staff", [
    # ID: HappyPath-1
    ("testuser", "Test", "test@example.com", "password123", True, False, False),
    # ID: HappyPath-2
    ("adminuser", "Admin", "admin@example.com", "adminpassword", True, True, True),
    # ID: EdgeCase-1 (Minimal info for a user)
    ("minimaluser", "Minimal", "minimal@example.com", "minimalpassword", True, False, False),
    # ID: ErrorCase-1 (Missing username)
    (None, "Error", "error@example.com", "errorpassword", True, False, False),
    # ID: ErrorCase-2 (Missing email)
    ("erroruser", "Error", None, "errorpassword", True, False, False),
])
def test_create_user(username, first_name, email, password, is_active, is_admin, is_staff):
    # Arrange
    # sourcery skip: no-conditionals-in-tests
    if username is None or email is None:
        with pytest.raises(ValueError):
            # Act
            User.objects.create_user(username=username, first_name=first_name, email=email,
                                     password=password, is_active=is_active, is_admin=is_admin,
                                     is_staff=is_staff)
    else:
        # Act
        user = User.objects.create_user(username=username, first_name=first_name, email=email,
                                        password=password, is_active=is_active, is_admin=is_admin,
                                        is_staff=is_staff)

        # Assert
        assert user.username == username
        assert user.first_name == first_name
        assert user.email == email
        assert user.check_password(password)
        assert user.is_active == is_active
        assert user.is_superuser == is_admin
        assert user.is_staff == is_staff


@pytest.mark.django_db
@pytest.mark.parametrize("api_key,api_secret,expiry,is_active", [
    # ID: HappyPath-1
    ("key123", "secret123", timezone.now() + timezone.timedelta(days=1), True),
    # ID: HappyPath-2
    ("key456", "secret456", None, False),
    # ID: EdgeCase-1 (Expiry in the past)
    ("key789", "secret789", timezone.now() - timezone.timedelta(days=1), True),
])
def test_server_side_credentials(api_key, api_secret, expiry, is_active):
    # Arrange
    user = User.objects.create_user(username="testuser", first_name="Test",
                                    email="test@example.com", password="password123")

    # Act
    credentials = ServerSideCredentials.objects.create(user=user, api_key=api_key,
                                                       api_secret=api_secret, expiry=expiry,
                                                       is_active=is_active)

    # Assert
    assert credentials.user == user
    assert credentials.api_key == api_key
    assert credentials.api_secret == api_secret
    assert credentials.expiry == expiry
    assert credentials.is_active == is_active
