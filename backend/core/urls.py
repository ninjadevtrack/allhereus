from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'login', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
    url(r'logout', views.logout_view, name="logout"),
    url(r'signup', views.signup, name='signup'),
    url(r'forgotpassword', views.forgotpassword, name='forgot_password'),

    url(r'profile$', views.profile, name='profile'),
    url(r'profile/edit', views.profile_edit, name='profile_edit'),

    url(r'checkins/$', views.checkins, name='checkins'),
    url(r'checkins/add', views.checkins_add, name='checkin_add'),
    url(r'checkins/(?P<id>[0-9]+)/$', views.checkin, name='checkin'),
    url(r'checkins/(?P<id>[0-9]+)/edit', views.checkin_edit, name='checkin_edit'),
    url(r'checkins.csv', views.checkins_csv, name='checkins_csv'),

    url(r'students/$', views.students, name='students'),
    url(r'students/add', views.student_add, name='student_add'),
    url(r'students/(?P<id>[0-9]+)/$', views.student, name='student'),
    url(r'students/(?P<id>[0-9]+)/edit', views.student_edit, name='student_edit'),

    url(r'teams/$', views.teams, name='teams'),
    url(r'teams/(?P<id>[0-9]+)/', views.team, name='team'),

    url(r'privacy', views.privacy, name='privacy'),
    url(r'support', views.support, name='support'),
]
