import hashlib

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None):
        """
        Creates and saves a User with the given email and password.
        """
        email = email or username
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        email = email or username
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserAH(AbstractBaseUser):
    """This is a bolt on for Django's underlying User model

    We use a OneToOneField to extend the Django auth user model. This allows
    us to store additional information that is linked to the User model.
    """

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    username = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def avatar_url(self):
        md5_email = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/' + md5_email + '?d=identicon'

    # def get_absolute_url(self):
    #     return reverse('users:detail', kwargs={'email': self.email})

    name = models.CharField(max_length=255, null=True, blank=True)
    hangout_email = models.EmailField(null=True, blank=True)

    # agreed to platform TOS and Privacy Policy
    agree_terms = models.BooleanField(default=False)
    agree_terms_at = models.DateTimeField(null=True, blank=True)

    school = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    grade = models.CharField(max_length=255, null=True, blank=True)
    content_area = models.CharField(max_length=255, null=True, blank=True)

    is_group_admin = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    avatar = models.CharField(max_length=255, blank=True, null=True)

    login_count = models.PositiveIntegerField(default=0)

    group = models.ForeignKey('Group', related_name='members', null=True, blank=True)
    teams = models.ManyToManyField('Team', related_name='members', blank=True)


class Group(BaseModel):
    """ All users must be a member of a Group

    This class can be thought of as a collection of users. Most commonly,
    Groups represent K12 districts or Universities.

    Note:
        Groups are not to be confused with Teams. Teams are groups of
        members within a group.
    """
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    email_root = models.CharField(max_length=255)

    is_school = models.BooleanField(default=False)
    is_district = models.BooleanField(default=False)
    is_university = models.BooleanField(default=False)
    is_charter = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.id is None:
            return '<Group ' + self.name + ' (unsaved)>'
        return '<Group ' + str(self.id) + ' ' + 'self.name'

    @property
    def users(self):
        return UserAH.objects.filter(group=self)


class Schools(BaseModel):
    """ Schools are sets of users within a Group

    Schools can only be associated w/ one Group
    Users can be part of multiple schools

    Example:
        For K12 groups, a teacher may be on a grade-level team as well as a
        content-based team.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    group = models.ForeignKey(Group)

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.id is None:
            return '<School ' + self.name + ' (unsaved)>'
        return '<School ' + str(self.id) + ' ' + 'self.name'


class Team(BaseModel):
    """ Teams are sets of users within a Group

    Users can be on multipe teams.

    Example:
        For K12 groups, a teacher may be on a grade-level team as well as a
        content-based team.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    group = models.ForeignKey(Group)

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.id is None:
            return '<Team ' + self.name + ' (unsaved)>'
        return '<Team ' + str(self.id) + ' ' + 'self.name'
