import pytest

pytestmark = pytest.mark.django_db

"""
Url tests for '/'
"""

def test_home_teacher(client, teacher):
    """
    route '/' for teacher
    """
    client.force_login(teacher)
    res = client.get('/')
    assert res.status_code == 200
  
def test_home_school_admin(client, school_admin):
    """
    route '/' for school admin
    """
    client.force_login(school_admin)
    res = client.get('/')
    assert res.status_code == 200

def test_home_district_admin(client, district_admin):
    """
    route '/' for district admin
    """
    client.force_login(district_admin)
    res = client.get('/')
    assert res.status_code == 200

def test_home_anonymous(client):
    """
    route '/' for anonymous user
    """
    res = client.get('/')
    assert res.status_code == 302


"""
Url tests for url(r'^schools/(?P<school_id>[0-9]+)/staff/(?P<staff_id>[0-9]+)/students/(?P<student_id>[0-9]+)/edit$', views.staff_student_edit, name='staff_student_edit'),
"""
def test_staff_student_edit_teacher(client, teacher, school, student):
    # teacher
    client.force_login(teacher)
    res = client.get('/schools/{}/staff/{}/students/{}/edit'.format(school.id, teacher.id, student.id))
    assert res.status_code == 403

def test_staff_student_edit_district_admin(client, district_admin, school, student):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/schools/{}/staff/{}/students/{}/edit'.format(school.id, district_admin.id, student.id))
    assert res.status_code == 200

def test_staff_student_edit_school_admin(client, school_admin, school, student):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/students/{}/edit'.format(school.id, school_admin.id, student.id))
    assert res.status_code == 403

def test_staff_student_edit_anonymous(client, school, student):
    # anonymous user
    res = client.get('/schools/{}/staff/1/students/{}/edit'.format(school.id, student.id))
    assert res.status_code == 302

"""
Url tests for url(r'^schools/(?P<school_id>[0-9]+)/staff/(?P<staff_id>[0-9]+)/students/(?P<student_id>[0-9]+)/$', views.staff_student, name='staff_student'),
"""
def test_staff_student_teacher(client, teacher, school, student):
    # teacher
    client.force_login(teacher)
    res = client.get('/schools/{}/staff/{}/students/{}/'.format(school.id, teacher.id, student.id))
    assert res.status_code == 403

def test_staff_student_school_admin(client, school_admin, school, student):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/students/{}/'.format(school.id, school_admin.id, student.id))
    assert res.status_code == 403

def test_staff_student_district_admin(client, district_admin, school, student):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/schools/{}/staff/{}/students/{}/'.format(school.id, district_admin.id, student.id))
    assert res.status_code == 200

def test_staff_student_anonymous(client, school, student):
    # anonymous user
    res = client.get('/schools/{}/staff/1/students/{}/'.format(school.id, student.id))
    assert res.status_code == 302


"""
Url tests for url(r'^schools/(?P<school_id>[0-9]+)/staff/(?P<staff_id>[0-9]+)/students/$', views.staff_students, name='staff_students'),
"""
def test_staff_students_teacher(client, teacher, school):
    # teacher
    client.force_login(teacher)
    res = client.get('/schools/{}/staff/{}/students/'.format(school.id, teacher.id))
    assert res.status_code == 403

def test_staff_students_school_admin(client, school_admin, school):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/students/'.format(school.id, school_admin.id))
    assert res.status_code == 403

def test_staff_students_district_admin(client, district_admin, school):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/schools/{}/staff/{}/students/'.format(school.id, district_admin.id))
    assert res.status_code == 200

def test_staff_students_anonymous(client, school):
    # anonymous user
    res = client.get('/schools/{}/staff/1/students/'.format(school.id))
    assert res.status_code == 302


"""
Url Tests url(r'^schools/(?P<school_id>[0-9]+)/staff/(?P<staff_id>[0-9]+)/password_set$', views.staff_password_set, name='staff_password_set'),
"""
def test_staff_password_set_teacher(client, teacher, school):
    # teacher
    client.force_login(teacher)
    res = client.get('/schools/{}/staff/{}/password_set'.format(school.id, teacher.id))
    assert res.status_code == 403

def test_staff_password_set_school_admin(client, school_admin, school):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/password_set'.format(school.id, school_admin.id))
    assert res.status_code == 403

def test_staff_password_set_district_admin(client, district_admin, school):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/schools/{}/staff/{}/password_set'.format(school.id, district_admin.id))
    assert res.status_code == 200

def test_staff_password_set_anonymous(client, school):
    # anonymous
    res = client.get('/schools/{}/staff/1/password_set'.format(school.id))
    assert res.status_code == 302

"""
Url Tests url(r'^schools/(?P<school_id>[0-9]+)/staff/(?P<staff_id>[0-9]+)/checkins/(?P<checkin_id>[0-9]+)/$', views.staff_checkin, name='staff_checkin'),
"""
def test_staff_checkin_teacher(client, teacher, school, checkin):
    # teacher
    client.force_login(teacher)
    res = client.get('/schools/{}/staff/{}/checkins/{}/'.format(school.id, teacher.id, checkin.id))
    assert res.status_code == 403

def test_staff_checkin_school_admin(client, school_admin, school, checkin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/checkins/{}/'.format(school.id, school_admin.id, checkin.id))
    assert res.status_code == 403

def test_staff_checkin_district_admin(client, district_admin, school, checkin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/schools/{}/staff/{}/checkins/{}/'.format(school.id, district_admin.id, checkin.id))
    assert res.status_code == 200

def test_staff_checkin_anonymous(client, school, checkin):
    # anonymous
    res = client.get('/schools/{}/staff/1/checkins/{}/'.format(school.id, checkin.id))
    assert res.status_code == 302

"""
Url Tests url(r'^schools/(?P<school_id>[0-9]+)/staff/(?P<staff_id>[0-9]+)/checkins/$', views.staff_checkins, name='staff_checkins'),
"""
def test_staff_checkins_teacher(client, teacher, school):
    # teacher
    client.force_login(teacher)
    res = client.get('/schools/{}/staff/{}/checkins/'.format(school.id, teacher.id))
    assert res.status_code == 403

def test_staff_checkins_school_admin(client, school_admin, school):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/checkins/'.format(school.id, school_admin.id))
    assert res.status_code == 403

def test_staff_checkins_district_admin(client, district_admin, school):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/schools/{}/staff/{}/checkins/'.format(school.id, district_admin.id))
    assert res.status_code == 200

def test_staff_checkins_anonymous(client, school):
    # anonymous
    res = client.get('/schools/{}/staff/1/checkins/'.format(school.id))
    assert res.status_code == 302

"""
Url Tests url(r'^schools/(?P<school_id>[0-9]+)/staff/(?P<staff_id>[0-9]+)/edit$', views.staff_profile_edit, name='staff_profile_edit'),
"""
def test_staff_profile_edit_teacher(client, teacher, school):
    # teacher
    client.force_login(teacher)
    res = client.get('/schools/{}/staff/{}/edit'.format(school.id, teacher.id))
    assert res.status_code == 403

def test_staff_profile_edit_school_admin(client, school_admin, school):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/edit'.format(school.id, school_admin.id))
    assert res.status_code == 403

def test_staff_profile_edit_district_admin(client, district_admin, school):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/schools/{}/staff/{}/edit'.format(school.id, district_admin.id))
    assert res.status_code == 200

def test_staff_profile_edit_anonymous(client, school):
    # anonymous
    res = client.get('/schools/{}/staff/1/edit'.format(school.id))
    assert res.status_code == 302

"""
Url Tests url(r'^schools/(?P<school_id>[0-9]+)/staff/(?P<staff_id>[0-9]+)/$', views.staff_profile, name='staff_profile'),
"""
def test_staff_profile_teacher(client, teacher, school):
    # teacher
    client.force_login(teacher)
    res = client.get('/schools/{}/staff/{}/'.format(school.id, teacher.id))
    assert res.status_code == 403

def test_staff_profile_school_admin(client, school_admin, school):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/'.format(school.id, school_admin.id))
    assert res.status_code == 403

def test_staff_profile_district_admin(client, district_admin, school):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/schools/{}/staff/{}/'.format(school.id, district_admin.id))
    assert res.status_code == 200

def test_staff_profile_anonymous(client, school):
    # anonymous
    res = client.get('/schools/{}/staff/1/'.format(school.id))
    assert res.status_code == 302

"""
Url Tests url(r'^schools/(?P<school_id>[0-9]+)/staff/$', views.staff, name='staff'),
"""
def test_staff_teacher(client, teacher, school):
    # teacher
    client.force_login(teacher)
    res = client.get('/schools/{}/staff/'.format(school.id, teacher.id))
    assert res.status_code == 403

def test_staff_school_admin(client, school_admin, school):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/'.format(school.id, school_admin.id))
    assert res.status_code == 403

def test_staff_district_admin(client, district_admin, school):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/schools/{}/staff/'.format(school.id, district_admin.id))
    assert res.status_code == 200

def test_staff_anonymous(client, school):
    # anonymous
    res = client.get('/schools/{}/staff/'.format(school.id))
    assert res.status_code == 302

"""
Url Tests url(r'schools/$', views.schools, name='schools'),
"""
def test_schools_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/schools/')
    assert res.status_code == 403

def test_schools_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/')
    assert res.status_code == 403

def test_schools_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/schools/')
    assert res.status_code == 200

def test_schools_anonymous(client):
    # anonymous
    res = client.get('/schools/')
    assert res.status_code == 302

"""
Url Tests url(r'profile$', views.profile, name='profile'),
"""
def test_profile_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/profile')
    assert res.status_code == 200

def test_profile_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/profile')
    assert res.status_code == 200

def test_profile_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/profile')
    assert res.status_code == 200

def test_profile_anonymous(client):
    # anonymous
    res = client.get('/profile')
    assert res.status_code == 302