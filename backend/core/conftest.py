import pytest

from .models import (
    CheckIn,
    MyUser,
    Student,
)


@pytest.fixture
def teacher():
    return MyUser.objects.create(
        email='teach@allhere.co',
        first_name='Donny',
        last_name='Donowitz')


@pytest.fixture
def student():
    return Student.objects.create(
        student_id=1338,
        first_name='Hans',
        last_name='Landa',
        language='German')


@pytest.fixture
def checkin(teacher, student):
    return CheckIn.objects.create(
        teacher=teacher,
        student=student)
