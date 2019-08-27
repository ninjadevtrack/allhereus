import pytest
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from .models import (
    CheckIn,
    MyUser,
    Student,
    District,
    School,
    Practice,
    Strategy,
)

@pytest.fixture
def district():
    return District.objects.create(
        name='mhps',
        email_contact='email@mhps.org')

@pytest.fixture
def school(district):
    return School.objects.create(
        name='middle school',
        address='123 school st',
        district=district)

@pytest.fixture
def teacher(school, district):
    u = MyUser.objects.create_user(
        email='teacher@allhere.co',
        first_name='Donny',
        last_name='Donowitz',
        password='test123',
        )
    u.district=district
    u.school=school
    u.save()
    return u

@pytest.fixture
def school_admin(school, district):
    u = MyUser.objects.create_user(
        email='schooladmin@allhere.co',
        first_name='School',
        last_name='Admin',
        password='test123',
        )
    u.district=district
    u.school=school
    u.role = 'SA'
    u.save()
    return u

@pytest.fixture
def district_admin(school, district):
    u = MyUser.objects.create_user(
        email='districtadmin@allhere.co',
        first_name='District',
        last_name='Admin',
        password='test123',
        )
    u.district=district
    u.school=school
    u.role = 'DA'
    u.save()
    return u

@pytest.fixture
def student(school, district, teacher):
    return Student.objects.create(
        student_id=1338,
        first_name='Hans',
        last_name='Landa',
        language='German',
        district=district,
        school=school,
        teacher=teacher)

@pytest.fixture
def checkin(teacher, student):
    return CheckIn.objects.create(
        teacher=teacher,
        student=student)

@pytest.fixture
def practice():
    return Practice.objects.create(
        name="Practice 1")

@pytest.fixture
def strategy(practice):
    return Strategy.objects.create(
        practice=practice,
        name="Test Strategy",
        display_name="Test Strategy Display Name",
        grade_level_from="k",
        grade_level_to="12")


@pytest.fixture
def flatpage_strategy_framework():
    try:
        site = Site.objects.get(pk=1)
    except Site.DoesNotExist:
        site = Site.objects.create(domain="app.allhere.co", name="allhere")
    try:
        flatpage = FlatPage.objects.get(url='/strategy-framework/')
    except FlatPage.DoesNotExist:
        flatpage = FlatPage.objects.create(
                url='/strategy-framework/',
                title="Library Framework",
                content="AllHere Library Strategy",
                registration_required=True,
                )
        flatpage.sites.add(site)
        flatpage.save()
        
                
