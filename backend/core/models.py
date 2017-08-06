import hashlib

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a user with given email and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model that only requires an email and password"""
    email = models.EmailField(unique=True)

    # Only use a single name because not everyone has both a first and last name
    full_name = models.CharField(max_length=255, null=True, blank=True)

    # required for admin
    is_active = models.BooleanField(
        default=True,
        help_text="Designates that this user account should be considered active. Users marked as inactive cannot login."
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates that this user can access the admin site.",
    )

    date_joined = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    # required for admin
    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # TODO: Add permissions
        return True

    # required for admin
    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # TODO: Add permissions
        return True

    @property
    def avatar_url(self):
        md5_email = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{md5_email}?d=identicon'

    @property
    def name(self):
        return self.full_name

    def __str__(self):
        return f'{self.full_name} <{self.email}>'
