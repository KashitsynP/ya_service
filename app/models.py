import re

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.timezone import now


class CustomUserManager(BaseUserManager):
    """Custom user manager that supports registration by email or phone."""

    def create_user(self, id, password, **extra_fields):
        """
        Creates and returns a user with the specified ID (email or phone)
        and password.
        """
        if not id:
            raise ValueError("The ID field must be set")

        user = self.model(id=id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, password, **extra_fields):
        """Creates and returns the superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    objects = CustomUserManager()

    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    PHONE_REGEX = r"^\+?\d{10,15}$"

    ID_TYPE_CHOICES = (
        ("email", "Email"),
        ("phone", "Phone"),
    )

    username = None
    id = models.CharField(
        primary_key=True,
        max_length=255,
        unique=True,
        help_text="Email or phone number",
    )
    id_type = models.CharField(
        max_length=10,
        choices=ID_TYPE_CHOICES,
        editable=False,
        help_text="Identifier type",
    )
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=now)

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        """Automatically detects ID type (email or phone)."""
        if re.match(self.EMAIL_REGEX, self.id):
            self.id_type = "email"
        elif re.match(self.PHONE_REGEX, self.id):
            self.id_type = "phone"
        else:
            raise ValueError("Invalid email or phone number")

            # We hash the password only if it has not yet been hashed
        if not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.id_type
