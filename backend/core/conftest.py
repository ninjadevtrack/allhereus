import pytest

from .models import (
    CheckIn,
    MyUser,
    Student,
    District,
    School,
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
