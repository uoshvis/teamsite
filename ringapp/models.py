from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        """Create and return a `Member` with an email, username and password."""
        if not email:
            raise ValueError('User must have a valid e-mail address')
        # Ensure that a username is set
        if not kwargs.get('username'):
            raise TypeError('Users must have a username.')

        user = self.model(
            username=kwargs.get('username'),
            email=self.normalize_email(email),
            firstname=kwargs.get('firstname', None),
            lastname=kwargs.get('lastname', None),
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **kwargs):
        """
        Create and return a `Member` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class Member(AbstractBaseUser, PermissionsMixin):

    firstname = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)

    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=50)

    role = models.CharField(max_length=100, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_short_name(self):
        # The user is identified by their username address
        return self.username
