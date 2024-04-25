from model_bakery import baker

from apps.auth_app.models import User

valid_user_data = baker.prepare(
    User, username="testuser", first_name="Test", email="valid@email.com", password="password123",
    is_active=True, is_admin=False, is_staff=False)
valid_user_data.save()

valid_admin_data = baker.prepare(
    User, username="adminuser", first_name="Admin", email="admin@emial.com",
    password="adminpassword", is_active=True, is_admin=True, is_staff=True)
valid_admin_data.save()

minimal_user_data = baker.prepare(
    User, username="minimaluser", first_name="Minimal", email="minimaluser@email.com",
    password="minimalpassword", is_active=True, is_admin=False, is_staff=False)
minimal_user_data.save()

invalid_user_data = baker.prepare(
    User, username=None, first_name="Error", email="error@email.com", password="errorpassword",
    is_active=True, is_admin=False, is_staff=False)
invalid_user_data.save()
