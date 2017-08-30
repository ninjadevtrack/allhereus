import hashlib

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None):
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

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)

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

    district = models.ForeignKey('District', related_name='members', null=True, blank=True)
    school = models.ForeignKey('School', related_name='members', null=True, blank=True)

    grade = models.CharField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)

    role = models.CharField(
        max_length=2,
        choices=(
            ('T', 'Teacher'),
            ('SA', 'School Admin'),
            ('DA', 'District Admin'),
        ),
        default='T',
        help_text='Account Type',
    )
    # if True, a user can edit membership
    is_manager = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}' if self.first_name and self.last_name else self.email

    def get_short_name(self):
        return self.first_name if self.first_name else self.email

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
    def is_school_admin(self):
        return self.role == 'SA'

    @property
    def is_district_admin(self):
        return self.role == 'DA'

    @property
    def checkins(self):
        if self.role == 'DA':
            return CheckIn.objects.filter(student__district=self.district).order_by('-date').all()
        if self.role == 'SA':
            return CheckIn.objects.filter(student__school=self.school).order_by('-date').all()
        else:
            return CheckIn.objects.filter(student__in=self.student_set.all()).order_by('-date').all()

    @property
    def students(self):
        if self.role == 'DA':
            return Student.objects.filter(district=self.district).order_by('-date').all()
        if self.role == 'SA':
            return Student.objects.filter(school=self.school).order_by('-date').all()
        else:
            return self.student_set.order_by('-date').all()

    @property
    def unassigned_students(self):
        if self.role == 'DA':
            return Student.objects.filter(district=self.district, teacher=None).order_by('last_name').all()
        # school admins and teachers
        else:
            return Student.objects.filter(school=self.school, teacher=None).order_by('last_name').all()

    @property
    def schools(self):
        return School.objects.all().filter(members=self)

    @property
    def avatar_url(self):
        md5_email = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        # we only want avatars rated G(`r=g`) https://secure.gravatar.com/site/implement/images/
        return f'https://www.gravatar.com/avatar/{md5_email}?d=identicon&r=g&s=75'

    @property
    def name(self):
        return self.get_full_name()

    def __str__(self):
        return self.get_full_name()


class CommonInfo(models.Model):
    """Abstract model for storing common model info"""
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Student(CommonInfo):
    """Student

    These are entities, not application users.
    """
    student_id = models.CharField(
        verbose_name='Student ID', null=True, blank=True,
        max_length=255, help_text='School identifier for student.')
    is_active = models.BooleanField(
        default=True, help_text='Designates that this student should be considered active.',)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    language = models.CharField(max_length=255, null=True, blank=True, help_text="Student/family's spoken language.",)
    email = models.EmailField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Contact email for student.',
    )

    # grade level of student
    grade = models.CharField(
        max_length=2,
        choices=(
            ('PK', 'Pre-Kindergarten'),
            ('K', 'Kindergarten'),
            ('1', '1st Grade'),
            ('2', '2nd Grade'),
            ('3', '3rd Grade'),
            ('4', '4th Grade'),
            ('5', '5th Grade'),
            ('6', '6th Grade'),
            ('7', '7th Grade'),
            ('8', '8th Grade'),
            ('9', '9th Grade'),
            ('10', '10th Grade'),
            ('11', '11th Grade'),
            ('12', '12th Grade'),
            ('O', 'Other')
        ),
        null=True,
        blank=True,
        help_text='Grade level of student.',
    )

    district = models.ForeignKey('District')
    school = models.ForeignKey('School')
    teacher = models.ForeignKey('MyUser', null=True, blank=True)

    parent_first_name = models.CharField(max_length=255, null=True, blank=True)
    parent_last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    parent_email = models.EmailField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Contact email for parent or guardian.',
    )

    @property
    def url(self):
        return reverse('student', args=[self.id])

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def checkins(self):
        return CheckIn.objects.order_by('-date').filter(student=self)

    @property
    def last_checkin(self):
        return self.checkins.first()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.name} <{self.student_id}>'


class CheckIn(CommonInfo):
    """CheckIn by teacher with student's family.

    In-school contact, phone call, or in-person visit.

    Three results:
    - a 1-10 score
    - text response of things learned
    - text response of ways to improve situation
    """
    date = models.DateTimeField(default=timezone.now, help_text='Date of check-in.')

    teacher = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, help_text='Person leading the check-in.')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, help_text='Student that check-in is on behalf of.',)
    status = models.CharField(
        max_length=1,
        choices=(
            ('C', 'Completed'),
            ('U', 'Unreachable'),
            ('M', 'Left Message'),
        ),
        blank=False,
        help_text='Current status of check-in.',
    )
    mode = models.CharField(
        max_length=1,
        choices=(
            ('P', 'Phone'),
            ('V', 'Visit'),
            ('I', 'In-Person')
        ),
        blank=False,
        help_text='Mode of communication for check-in.',
    )
    notify_school_admin = models.BooleanField(
        default=False, help_text='Should school administrator be notified?',)
    success_score = models.PositiveIntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        help_text='Scale (1-10) of check-in success.',
    )
    info_learned = models.TextField(
        verbose_name='Information Gathered',
        null=True,
        blank=True,
        help_text='Most important thing you learned about your mentee at your most recent mentoring check-in.',
    )
    info_better = models.TextField(
        verbose_name='Improvements for Future',
        null=True,
        blank=True,
        help_text='What could have made this mentor check-in better?',
    )

    @property
    def district(self):
        return self.student.district

    @property
    def school(self):
        return self.student.school

    @property
    def url(self):
        return reverse('checkin', args=[self.id])

    def __str__(self):
        return f'Check-in on {self.student} by {self.teacher} at {self.date}'


class District(CommonInfo):
    """Collection of users representing K12 district or university.

    Users/Students are associated with _one_ District
    """
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(
        default=True, help_text='Designates that this Team should be considered active.',)
    state = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        help_text='State where District/University is headquartered.'
    )
    email_contact = models.EmailField(
        max_length=255, unique=False, help_text='Email for District/University contact.')

    is_charter = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)

    notes = models.TextField(null=True, blank=True)

    custom_text_succces_score = models.TextField(null=True, blank=True)
    custom_text_info_learned = models.TextField(null=True, blank=True)
    custom_text_info_better = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class School(CommonInfo):
    """Collection of users within a District

    Schools can be associated with _one_ District
    Users can be associated with _multiple_ Schools
    Students can be associated with _one_ School
    """
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(
        default=True, help_text='Designates that this Team should be considered active.',)
    address = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    district = models.ForeignKey(District)

    def __str__(self):
        return self.name
