from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.home),

    url(r'login', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
    url(r'logout', auth_views.logout, name="logout"),
    url(r'signup', views.signup),
    url(r'forgotpassword', views.forgotpassword, name='forgot_password'),

    url(r'profile$', views.profile),
    url(r'profile/edit', views.profile_edit),

    url(r'checkins/$', views.checkins),
    url(r'checkins/add', views.checkins_add),
    url(r'checkins/(?P<id>[0-9]+)/', views.checkin),
    url(r'checkins/(?P<id>[0-9]+)/edit', views.checkin_edit),

    url(r'teams/$', views.teams),
    url(r'teams/(?P<id>[0-9]+)/', views.team),
]
