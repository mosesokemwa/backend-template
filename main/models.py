from datetime import datetime
from typing import Any, Optional

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('User must have a valid email')

        email = self.normalize_email(email)
        user = self.model(email=email, created_at=datetime.now(), must_change_password=True, deleted=False, **extra_fields)
        user.first_name = first_name
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(email, password, first_name, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def normalize_email(self, email):
        return email.lower()

    def get_by_natural_key(self, email):
        return self.get(email=email)


class UserModel(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'password']

    objects = UserManager()

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254, unique=True, null=False, blank=False)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=254, null=True, blank=True)
    middle_name = models.CharField(max_length=254, blank=True)
    last_name = models.CharField(max_length=254, blank=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    dob = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=254, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def has_module_perms(self, app_label):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return self.is_superuser


class ResidentialAddressModel(models.Model):
    # user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    # one to one with user model
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=254, blank=True)
    country = models.CharField(max_length=254, blank=True)
    state = models.CharField(max_length=254, blank=True)
    city = models.CharField(max_length=254, blank=True)
    zip = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Residential Address'
        verbose_name_plural = 'Residential Addresses'
