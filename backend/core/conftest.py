import pytest

from .models import (
    CheckIn,
    MyUser,
    Student,
    District,
    School,
)


@pytest.fixture
def teacher():
    return MyUser.objects.create_user(
        email='teach@allhere.co',
        first_name='Donny',
        last_name='Donowitz',
        password='test123'
        )


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
def school(district):
    return School.objects.create(
        name='middle school',
        address='123 school st',
        district=district)


@pytest.fixture
def district():
    return District.objects.create(
        name='mhps',
        email_contact='email@mhps.org')


@pytest.fixture
def checkin(teacher, student):
    return CheckIn.objects.create(
        teacher=teacher,
        student=student)
