from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager


class UserAccountManager(BaseUserManager):

    def _create_user(self, email: str, password: str = None, **extra_fields):
        """
        create and saves a User with given email and password
        """
        if not email:
            raise ValueError("Users must have an email address.")

        if not password:
            raise ValueError("User must set a password")

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str = None, **extra_fields):
        """
        create and save a user with given email and password
        """
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_admin", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        create and save a superuser with given email and password
        """
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must has is_superuser=True")
        return self._create_user(email, password, **extra_fields)
