"""
Models for Profiles.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for User profiles"""

    def create_user(self, email, first_name, last_name=None, password=None):
        """Creates a new User profile"""
        if not email:
            raise ValueError('Email of the user is required to be provided')

        if not first_name:
            raise ValueError(
                'First name of the user is required to be provided'
            )

        user = self.model(
                email=self.normalize_email(email),
                first_name=first_name,
                last_name=last_name,
            )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, password, last_name=None):
        """Creates a superuser in the system"""
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Model class for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def get_full_name(self):
        """Get user's full name"""
        if self.last_name is not None:
            return self.first_name + " " + self.last_name
        else:
            return self.first_name

    def get_short_name(self):
        """Get user's short name"""
        return self.first_name

    def __str__(self):
        """Get the string representation of User model"""
        return self.email


class ProfileFeedItem(models.Model):
    """Profile status updates"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation"""
        return self.status_text
