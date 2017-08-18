from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'login', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
    url(r'logout', views.logout_view, name="logout"),
    url(r'signup', views.signup, name='signup'),
    url(r'^password_change/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change'),
    url(r'^password_change/done/$', auth_views.PasswordChangeView.as_view(), name='password_change_done'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'), name="password_reset"),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    url(r'profile$', views.profile, name='profile'),
    url(r'profile/edit', views.profile_edit, name='profile_edit'),

    url(r'checkins/$', views.checkins, name='checkins'),
    url(r'checkins/add', views.checkins_add, name='checkin_add'),
    url(r'checkins/(?P<id>[0-9]+)/$', views.checkin, name='checkin'),
    url(r'checkins/(?P<id>[0-9]+)/edit', views.checkin_edit, name='checkin_edit'),
    url(r'checkins/(?P<id>[0-9]+)/delete', views.checkin_delete, name='checkin_delete'),
    url(r'checkins.csv', views.checkins_csv, name='checkins_csv'),

    url(r'students/$', views.students, name='students'),
    url(r'students/add', views.student_add, name='student_add'),
    url(r'students/unassigned', views.students_unassigned, name='students_unassigned'),
    url(r'students/(?P<id>[0-9]+)/$', views.student, name='student'),
    url(r'students/(?P<id>[0-9]+)/edit', views.student_edit, name='student_edit'),

    url(r'teams/$', views.teams, name='teams'),
    url(r'teams/(?P<id>[0-9]+)/', views.team, name='team'),

    url(r'privacy', views.privacy, name='privacy'),
    url(r'support', views.support, name='support'),
]
