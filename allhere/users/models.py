import hashlib

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
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
    active = models.BooleanField(default=True)

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
        return self.name

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

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'pk': self.id})

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    # agreed to platform TOS and Privacy Policy
    agree_terms = models.BooleanField(default=False)
    agree_terms_at = models.DateTimeField(null=True, blank=True)

    school = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    grade = models.CharField(max_length=255, null=True, blank=True)
    content_area = models.CharField(max_length=255, null=True, blank=True)

    is_manager = models.BooleanField(default=False)
    is_leader = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=True)

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
    active = models.BooleanField(default=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    email_contact = models.EmailField(
                                verbose_name='email contact',
                                max_length=255,
                                unique=False,
                            )
    
    is_charter = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)

    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.id is None:
            return '<Group ' + self.name + ' (unsaved)>'
        return '<Group ' + str(self.id) + ' ' + 'self.name'

    @property
    def users(self):
        return UserAH.objects.filter(group=self)


class School(BaseModel):
    """ Schools are sets of users within a Group

    Schools can only be associated w/ one Group
    Users can be part of multiple schools
    """
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    description = models.TextField()
    active = models.BooleanField(default=True)

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
    active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    group = models.ForeignKey(Group)

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.id is None:
            return '<Team ' + self.name + ' (unsaved)>'
        return '<Team ' + str(self.id) + ' ' + 'self.name'


class Student(BaseModel):
    """Represents a Student

    Note: These individuals never log in
    """
    student_id = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # this is the student and/or student's family's spoken language
    language = models.CharField(max_length=255)

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    Grade = models.CharField(max_length=2, choices=(
        ('PK', 'Pre-Kindergarten'),
        ('K', 'Kindergarten'), ('1', '1st Grade'), ('2', '2nd Grade'), ('3', '3rd Grade'), ('4', '4th Grade'), ('5', '5th Grade'),
        ('6', '6th Grade'), ('7', '7th Grade'), ('8', '8th Grade'),
        ('9', '9th Grade'), ('10', '10th Grade'), ('11', '11th Grade'), ('12', '12th Grade'), ('O', 'Other')
    ), null=True, blank=True)

    group = models.ForeignKey(Group)
    school = models.ForeignKey(School)
    team = models.ForeignKey(Team)

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name
    
    def __str__(self):
        return self.name


class Attendance(BaseModel):
    """Captures info around absences and tardies

    Note: This class doesn't inherit from the BaseModel like others
    """
    date = models.DateTimeField()
    absence = models.PositiveIntegerField(default=0)
    tardies = models.PositiveIntegerField(default=0)

    student = models.ForeignKey(Student)

class CheckIn(BaseModel):
    """
    Teachers lead checkins with a student's family.

    These checkins can happen in-person at the school, over the phone, or with
    the teacher visiting the family somewhere.

    It results in 3 entites:
        1) a 1-10 score
        2) text response of things learned
        3) text with ways to improve situation 
    """
    date = models.DateTimeField()
    # this is the person leading the meeting
    teacher = models.ForeignKey('UserAH')
    # this is the student that the meeting is on the behalf of
    student = models.ForeignKey('Student')
    # what is the current status of the checkin
    status = models.CharField(max_length=1, choices=(
        ('C', 'Completed'), ('U', 'Unreachable'), ('M', 'Left Message')
    ), null=True, blank=True)
    # how was the checkin conducted
    format = models.CharField(max_length=1, choices=(
        ('P', 'Phone'), ('V', 'Visit'), ('I', 'In-Person')
    ), null=True, blank=True)

    # should_notify_school_admin
    should_notify_school_admin = models.BooleanField(default=False)

    # (1 to 10) How successful was the recent check-in you had with your mentee?
    success_score = models.PositiveIntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    # What is the most important thing you learned about your mentee at your most recent mentoring check-in?
    things_learned = models.TextField(null=True, blank=True)
    # What could have made this mentor check-in better? *
    how_better = models.TextField(null=True, blank=True)

class CheckInFormText(BaseModel):
    """
    This field will allow groups to customize the form text.

    For some groups, the admins/teachers may want to word the form's
    prompts differently
    """

    group = models.ForeignKey('Group')

    success_score_text = models.TextField(null=True, blank=True)
    things_learned_text = models.TextField(null=True, blank=True)
    how_better_text = models.TextField(null=True, blank=True)
