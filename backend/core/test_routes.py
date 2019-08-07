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
    assert res.status_code == 404

def test_staff_student_edit_district_admin(client, district_admin, school, student):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/schools/{}/staff/{}/students/{}/edit'.format(school.id, district_admin.id, student.id))
    assert res.status_code == 200

def test_staff_student_edit_school_admin(client, school_admin, school, student):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/students/{}/edit'.format(school.id, school_admin.id, student.id))
    assert res.status_code == 200

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
    assert res.status_code == 404

def test_staff_student_school_admin(client, school_admin, school, student):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/students/{}/'.format(school.id, school_admin.id, student.id))
    assert res.status_code == 200

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
    assert res.status_code == 404

def test_staff_students_school_admin(client, school_admin, school):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/students/'.format(school.id, school_admin.id))
    assert res.status_code == 200

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
    assert res.status_code == 404

def test_staff_checkin_school_admin(client, school_admin, school, checkin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/checkins/{}/'.format(school.id, school_admin.id, checkin.id))
    assert res.status_code == 200

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
    assert res.status_code == 404

def test_staff_checkins_school_admin(client, school_admin, school):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/checkins/'.format(school.id, school_admin.id))
    assert res.status_code == 200

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
    assert res.status_code == 404

def test_staff_profile_edit_school_admin(client, school_admin, school):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/edit'.format(school.id, school_admin.id))
    assert res.status_code == 200

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
    assert res.status_code == 404

def test_staff_profile_school_admin(client, school_admin, school):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/{}/'.format(school.id, school_admin.id))
    assert res.status_code == 200

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
    assert res.status_code == 404

def test_staff_school_admin(client, school_admin, school):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/{}/staff/'.format(school.id, school_admin.id))
    assert res.status_code == 200

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
    assert res.status_code == 404

def test_schools_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/schools/')
    assert res.status_code == 200

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

"""
Url Tests url(r'login', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
"""
def test_login_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/login')
    assert res.status_code == 200

def test_login_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/login')
    assert res.status_code == 200

def test_login_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/login')
    assert res.status_code == 200

def test_login_anonymous(client):
    # anonymous
    res = client.get('/login')
    assert res.status_code == 200

"""
Url Tests url(r'logout', views.logout_view, name="logout"),
"""
def test_logout_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/logout')
    assert res.status_code == 302 and res.url == '/'

def test_logout_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/logout')
    assert res.status_code == 302 and res.url == '/'

def test_logout_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/logout')
    assert res.status_code == 302 and res.url == '/'

def test_logout_anonymous(client):
    # anonymous
    res = client.get('/logout')
    assert res.status_code == 302 and res.url == '/'

"""
Url Tests url(r'^password_change/$', auth_views.PasswordChangeView.as_view(template_name='core/password_change.html'), name='password_change'),
"""
def test_password_change_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/password_change/')
    assert res.status_code == 200
def test_password_change_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/password_change/')
    assert res.status_code == 200

def test_password_change_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/password_change/')
    assert res.status_code == 200
def test_password_change_anonymous(client):
    # anonymous
    res = client.get('/password_change/')
    assert res.status_code == 302 and res.url == '/login?next=/password_change/'

"""
Url Tests url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='core/password_change_done.html'), name='password_change_done'),
"""
def test_password_change_done_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/password_change/done/')
    assert res.status_code == 200
def test_password_change_done_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/password_change/done/')
    assert res.status_code == 200

def test_password_change_done_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/password_change/done/')
    assert res.status_code == 200
def test_password_change_done_anonymous(client):
    # anonymous
    res = client.get('/password_change/done/')
    assert res.status_code == 302 and res.url == '/login?next=/password_change/done/'

"""
Url Tests url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'), name="password_reset"),
"""
def test_password_reset_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/password_reset/')
    assert res.status_code == 200
def test_password_reset_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/password_reset/')
    assert res.status_code == 200

def test_password_reset_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/password_reset/')
    assert res.status_code == 200
def test_password_reset_anonymous(client):
    # anonymous
    res = client.get('/password_reset/')
    assert res.status_code == 200

"""
Url Tests url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
"""
def test_password_reset_done_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/password_reset/done/')
    assert res.status_code == 200
def test_password_reset_done_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/password_reset/done/')
    assert res.status_code == 200

def test_password_reset_done_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/password_reset/done/')
    assert res.status_code == 200
def test_password_reset_done_anonymous(client):
    # anonymous
    res = client.get('/password_reset/done/')
    assert res.status_code == 200

"""
Url Tests url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),
"""
def test_reset_done_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/reset/done/')
    assert res.status_code == 200
def test_reset_done_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/reset/done/')
    assert res.status_code == 200

def test_reset_done_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/reset/done/')
    assert res.status_code == 200
def test_reset_done_anonymous(client):
    # anonymous
    res = client.get('/reset/done/')
    assert res.status_code == 200

"""
Url Tests url(r'^profile/edit', views.profile_edit, name='profile_edit'),
"""
def test_profile_edit_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/profile/edit')
    assert res.status_code == 200
def test_profile_edit_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/profile/edit')
    assert res.status_code == 200

def test_profile_edit_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/profile/edit')
    assert res.status_code == 200
def test_profile_edit_anonymous(client):
    # anonymous
    res = client.get('/profile/edit')
    assert res.status_code == 302 and res.url == '/login?next=/profile/edit'

"""
Url Tests url(r'^checkins/$', views.checkins, name='checkins'),
"""
def test_checkins_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/checkins/')
    assert res.status_code == 200
def test_checkins_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/checkins/')
    assert res.status_code == 200

def test_checkins_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/checkins/')
    assert res.status_code == 200

def test_checkins_anonymous(client):
    # anonymous
    res = client.get('/checkins/')
    assert res.status_code == 302 and res.url == '/login?next=/checkins/'

"""
Url Tests url(r'^checkins/add', views.checkins_add, name='checkin_add'),
"""
def test_checkins_add_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/checkins/add')
    assert res.status_code == 200
def test_checkins_add_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/checkins/add')
    assert res.status_code == 200

def test_checkins_add_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/checkins/add')
    assert res.status_code == 404
def test_checkins_add_anonymous(client):
    # anonymous
    res = client.get('/checkins/add')
    assert res.status_code == 302 and res.url == '/login?next=/checkins/add'

"""
Url Tests url(r'^checkins/(?P<id>[0-9]+)/$', views.checkin, name='checkin'),
"""
def test_checkins_add_teacher(client, teacher, checkin):
    # teacher
    client.force_login(teacher)
    res = client.get('/checkins/{}/'.format(checkin.id))
    assert res.status_code == 200
def test_checkins_add_school_admin(client, school_admin, checkin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/checkins/{}/'.format(checkin.id))
    assert res.status_code == 200

def test_checkins_add_district_admin(client, district_admin, checkin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/checkins/{}/'.format(checkin.id))
    assert res.status_code == 200
def test_checkins_add_anonymous(client, checkin):
    # anonymous
    res = client.get('/checkins/{}/'.format(checkin.id))
    assert res.status_code == 302 and res.url == '/login?next=/checkins/{}/'.format(checkin.id)


"""
Url Tests url(r'^checkins/(?P<id>[0-9]+)/edit', views.checkin_edit, name='checkin_edit'),
"""
def test_checkins_edit_teacher(client, teacher, checkin):
    # teacher
    client.force_login(teacher)
    res = client.get('/checkins/{}/edit'.format(checkin.id))
    assert res.status_code == 200
def test_checkins_edit_school_admin(client, school_admin, checkin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/checkins/{}/edit'.format(checkin.id))
    assert res.status_code == 200

def test_checkins_edit_district_admin(client, district_admin, checkin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/checkins/{}/edit'.format(checkin.id))
    assert res.status_code == 200
def test_checkins_edit_anonymous(client, checkin):
    # anonymous
    res = client.get('/checkins/{}/edit'.format(checkin.id))
    assert res.status_code == 302 and res.url == '/login?next=/checkins/{}/edit'.format(checkin.id)

    """
Url Tests url(r'^checkins/(?P<id>[0-9]+)/delete', views.checkin_delete, name='checkin_delete'),
"""
def test_checkins_delete_teacher(client, teacher, checkin):
    # teacher
    client.force_login(teacher)
    res = client.get('/checkins/{}/delete'.format(checkin.id))
    assert res.status_code == 200
def test_checkins_delete_school_admin(client, school_admin, checkin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/checkins/{}/delete'.format(checkin.id))
    assert res.status_code == 200

def test_checkins_delete_district_admin(client, district_admin, checkin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/checkins/{}/delete'.format(checkin.id))
    assert res.status_code == 200
def test_checkins_delete_anonymous(client, checkin):
    # anonymous
    res = client.get('/checkins/{}/delete'.format(checkin.id))
    assert res.status_code == 302 and res.url == '/login?next=/checkins/{}/delete'.format(checkin.id)

"""
Url Tests url(r'^students/$', views.students, name='students'),
"""
def test_students_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/students/')
    assert res.status_code == 200
def test_students_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/students/')
    assert res.status_code == 404

def test_students_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/students/')
    assert res.status_code == 200
def test_students_anonymous(client):
    # anonymous
    res = client.get('/students/')
    assert res.status_code == 302 and res.url == '/login?next=/students/'

"""
Url Tests url(r'^students/unassigned', views.students_unassigned, name='students_unassigned'),
"""
def test_students_unassigned_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/students/unassigned')
    assert res.status_code == 200
def test_students_unassigned_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/students/unassigned')
    assert res.status_code == 404

def test_students_unassigned_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/students/unassigned')
    assert res.status_code == 200
def test_students_unassigned_anonymous(client):
    # anonymous
    res = client.get('/students/unassigned')
    assert res.status_code == 302 and res.url == '/login?next=/students/unassigned'

"""
Url Tests url(r'^students/(?P<id>[0-9]+)/$', views.student, name='student'),
"""
def test_student_teacher(client, teacher, student):
    # teacher
    client.force_login(teacher)
    res = client.get('/students/{}/'.format(student.id))
    assert res.status_code == 200
def test_student_school_admin(client, school_admin, student):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/students/{}/'.format(student.id))
    assert res.status_code == 404

def test_student_district_admin(client, district_admin, student):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/students/{}/'.format(student.id))
    assert res.status_code == 200
def test_student_anonymous(client, student):
    # anonymous
    res = client.get('/students/{}/'.format(student.id))
    assert res.status_code == 302 and res.url == '/login?next=/students/{}/'.format(student.id)

"""
Url Tests url(r'^students/(?P<id>[0-9]+)/edit$', views.student, name='student'),
"""
def test_student_teacher(client, teacher, student):
    # teacher
    client.force_login(teacher)
    res = client.get('/students/{}/edit'.format(student.id))
    assert res.status_code == 200
def test_student_school_admin(client, school_admin, student):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/students/{}/edit'.format(student.id))
    assert res.status_code == 404

def test_student_district_admin(client, district_admin, student):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/students/{}/edit'.format(student.id))
    assert res.status_code == 200
def test_student_anonymous(client, student):
    # anonymous
    res = client.get('/students/{}/edit'.format(student.id))
    assert res.status_code == 302 and res.url == '/login?next=/students/{}/edit'.format(student.id)

"""
Url Tests url(r'^students.pdf', views.students_pdf, name='students_pdf'),
"""
def test_students_pdf_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/students.pdf')
    assert res.status_code == 200

def test_students_pdf_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/students.pdf')
    assert res.status_code == 200

def test_students_pdf_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/students.pdf')
    assert res.status_code == 404

def test_students_pdf_anonymous(client):
    # anonymous
    res = client.get('/students.pdf')
    assert res.status_code == 302

"""
Url Tests url(r'^students.csv', views.students_csv, name='students_csv'),
"""
def test_students_csv_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/students.csv')
    assert res.status_code == 200

def test_students_csv_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/students.csv')
    assert res.status_code == 200

def test_students_csv_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/students.csv')
    assert res.status_code == 404

def test_students_csv_anonymous(client):
    # anonymous
    res = client.get('/students.csv')
    assert res.status_code == 302


"""
Url Tests url(r'^checkins.pdf', views.checkins_pdf, name='checkins_pdf'),
"""
def test_checkins_pdf_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/checkins.pdf')
    assert res.status_code == 200

def test_checkins_pdf_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/checkins.pdf')
    assert res.status_code == 200

def test_checkins_pdf_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/checkins.pdf')
    assert res.status_code == 200

def test_checkins_pdf_anonymous(client):
    # anonymous
    res = client.get('/checkins.pdf')
    assert res.status_code == 302

"""
Url Tests url(r'^checkins.csv', views.checkins_csv, name='checkins_csv'),
"""
def test_checkins_csv_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/checkins.csv')
    assert res.status_code == 200

def test_checkins_csv_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/checkins.csv')
    assert res.status_code == 200

def test_checkins_csv_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/checkins.csv')
    assert res.status_code == 200

def test_checkins_csv_anonymous(client):
    # anonymous
    res = client.get('/checkins.csv')
    assert res.status_code == 302

"""
Url Tests url(r'reports/$', views.reports, name='reports'),
"""
def test_reports_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/reports/')
    assert res.status_code == 200

def test_reports_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/reports/')
    assert res.status_code == 200

def test_reports_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/reports/')
    assert res.status_code == 200

def test_reports_anonymous(client):
    # anonymous
    res = client.get('/reports/')
    assert res.status_code == 302


"""
Url Tests url(r'reports-chart/$', views.reports_in_chart, name='reports-chart'),
"""
def test_reports_chart_teacher(client, school, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get(f'/reports-chart/?school={school.id}')
    assert res.status_code == 200

def test_reports_chart_school_admin(client, school, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get(f'/reports-chart/?school={school.id}')
    assert res.status_code == 200

def test_reports_chart_district_admin(client, school, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get(f'/reports-chart/?school={school.id}')
    assert res.status_code == 200

def test_reports_chart_anonymous(client, school):
    # anonymous
    res = client.get(f'/reports-chart/?school={school.id}')
    assert res.status_code == 302


"""
Url Tests url(r'teams/$', views.teams, name='teams'),
"""
def test_teams_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/teams/')
    assert res.status_code == 200

def test_teams_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/teams/')
    assert res.status_code == 200

def test_teams_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/teams/')
    assert res.status_code == 200

def test_teams_anonymous(client):
    # anonymous
    res = client.get('/teams/')
    assert res.status_code == 302


"""
Url Tests url(r'support', views.support, name='support'),
"""
def test_support_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/support')
    assert res.status_code == 200

def test_support_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/support')
    assert res.status_code == 200

def test_support_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/support')
    assert res.status_code == 200

def test_support_anonymous(client):
    # anonymous
    res = client.get('/support')
    assert res.status_code == 200

"""
Url Tests url(r'privacy', views.privacy, name='privacy'),
"""
def test_privacy_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/privacy')
    assert res.status_code == 200

def test_privacy_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/privacy')
    assert res.status_code == 200

def test_privacy_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/privacy')
    assert res.status_code == 200

def test_privacy_anonymous(client):
    # anonymous
    res = client.get('/privacy')
    assert res.status_code == 200

"""
Url Tests url(r'teams/(?P<id>[0-9]+)/', views.team, name='team'),
"""
def test_team_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/teams/123/')
    assert res.status_code == 200

def test_team_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/teams/123/')
    assert res.status_code == 200

def test_team_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/teams/123/')
    assert res.status_code == 200

def test_team_anonymous(client):
    # anonymous
    res = client.get('/teams/123/')
    assert res.status_code == 302

"""
Url Tests url(r'/library/$', views.library, name='library')
"""
def test_library_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/library/')
    assert res.status_code == 200

def test_library_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/library/')
    assert res.status_code == 200

def test_library_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/library/')
    assert res.status_code == 200

def test_library_anonymous(client):
    # anonymous
    res = client.get('/library/')
    assert res.status_code == 302

"""
Url Tests url(r'/strategies/$', views.strategies, name='strategies')
"""
def test_strategies_teacher(client, teacher):
    # teacher
    client.force_login(teacher)
    res = client.get('/strategies/')
    assert res.status_code == 200

def test_strategies_school_admin(client, school_admin):
    # school_admin
    client.force_login(school_admin)
    res = client.get('/strategies/')
    assert res.status_code == 200

def test_strategies_district_admin(client, district_admin):
    # district_admin
    client.force_login(district_admin)
    res = client.get('/strategies/')
    assert res.status_code == 200

def test_strategies_anonymous(client):
    # anonymous
    res = client.get('/strategies/')
    assert res.status_code == 302

"""
Url Tests url(r'^strategies/(?P<strategy_id>[a-z0-9\-]+)/$', views.strategy, name='strategy')
"""
def test_strategy_teacher(client, teacher, strategy):
    # teacher
    client.force_login(teacher)
    res = client.get(f'/strategies/{strategy.id}/')
    assert res.status_code == 200

def test_strategy_school_admin(client, school_admin, strategy):
    # school_admin
    client.force_login(school_admin)
    res = client.get(f'/strategies/{strategy.id}/')
    assert res.status_code == 200

def test_strategy_district_admin(client, district_admin, strategy):
    # district_admin
    client.force_login(district_admin)
    res = client.get(f'/strategies/{strategy.id}/')
    assert res.status_code == 200

def test_strategy_anonymous(client, strategy):
    # anonymous
    res = client.get(f'/strategies/{strategy.id}/')
    assert res.status_code == 302


"""
Url Tests url(r'^library/framework/$', flagepge_view.library_framework, name='library_framework')
"""
def test_library_framework_teacher(client, teacher, flatpage_library_framework):
    # teacher
    client.force_login(teacher)
    res = client.get(f'/library/framework/')
    assert res.status_code == 200

def test_library_framework_school_admin(client, school_admin, flatpage_library_framework):
    # school_admin
    client.force_login(school_admin)
    res = client.get(f'/library/framework/')
    assert res.status_code == 200

def test_library_framework_district_admin(client, district_admin, flatpage_library_framework):
    # district_admin
    client.force_login(district_admin)
    res = client.get(f'/library/framework/')
    assert res.status_code == 200

def test_library_framework_anonymous(client, flatpage_library_framework):
    # anonymous
    res = client.get(f'/library/framework/')
    assert res.status_code == 302

"""
url(r'^schools/(?P<school_id>[0-9]+)/staff.json$', views.schools_staff_json, name='schools_staff_json'),
"""
def test_schools_staff_json_teacher(client, teacher, school):
    # teacher
    client.force_login(teacher)
    res = client.get(f'/schools/{school.id}/staff.json')
    assert res.status_code == 200

def test_schools_staff_json_school_admin(client, school_admin, school, teacher):
    # school_admin
    client.force_login(school_admin)
    res = client.get(f'/schools/{school.id}/staff.json')
    assert res.status_code == 200

def test_schools_staff_json_district_admin(client, district_admin, school, teacher):
    # district_admin
    client.force_login(district_admin)
    res = client.get(f'/schools/{school.id}/staff.json')
    assert res.status_code == 200

def test_schools_staff_json_anonymous(client, school, teacher):
    # anonymous
    res = client.get(f'/schools/{school.id}/staff.json')
    assert res.status_code == 302


"""
url(r'^schools/(?P<school_id>[0-9]+)/staff/(?P<teacher_id>[0-9]+)/students.json$', views.schools_staff_students_json, name='schools_staff_students_json'),
"""
def test_schools_staff_students_json_teacher(client, teacher, school):
    # teacher
    client.force_login(teacher)
    res = client.get(f'/schools/{school.id}/staff/{teacher.id}/students.json')
    assert res.status_code == 200

def test_schools_staff_students_json_school_admin(client, school_admin, school, teacher):
    # school_admin
    client.force_login(school_admin)
    res = client.get(f'/schools/{school.id}/staff/{teacher.id}/students.json')
    assert res.status_code == 200

def test_schools_staff_students_json_district_admin(client, district_admin, school, teacher):
    # district_admin
    client.force_login(district_admin)
    res = client.get(f'/schools/{school.id}/staff/{teacher.id}/students.json')
    assert res.status_code == 200

def test_schools_staff_students_json_anonymous(client, school, teacher):
    # anonymous
    res = client.get(f'/schools/{school.id}/staff/{teacher.id}/students.json')
    assert res.status_code == 302


"""
url(r'^schools/(?P<school_id>[0-9]+)/students.json$', views.schools_students_json, name='schools_students_json'),
"""
def test_schools_students_json_teacher(client, teacher, school):
    # teacher
    client.force_login(teacher)
    res = client.get(f'/schools/{school.id}/students.json')
    assert res.status_code == 200

def test_schools_students_json_school_admin(client, school_admin, school):
    # school_admin
    client.force_login(school_admin)
    res = client.get(f'/schools/{school.id}/students.json')
    assert res.status_code == 200

def test_schools_students_json_district_admin(client, district_admin, school):
    # district_admin
    client.force_login(district_admin)
    res = client.get(f'/schools/{school.id}/students.json')
    assert res.status_code == 200

def test_schools_students_json_anonymous(client, school):
    # anonymous
    res = client.get(f'/schools/{school.id}/students.json')
    assert res.status_code == 302
