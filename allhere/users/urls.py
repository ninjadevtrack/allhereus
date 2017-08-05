from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^users/$', view=views.UserListView.as_view(), name='user_list'),
    url(r'^users/(?P<pk>[\w.@+-]+)/$', view=views.UserDetailView.as_view(), name='user_profile'),
    url(r'^users/redirect/$', view=views.UserRedirectView.as_view(), name='redirect'),
    url(r'^~update/$', view=views.UserUpdateView.as_view(), name='update'),
    url(r'^checkins/$', views.CheckInList.as_view(), name='checkin_list'),
    url(r'^checkins/new$', views.CheckInCreate.as_view(), name='checkin_new'),
    url(r'^checkins/edit/(?P<pk>\d+)$', views.CheckInUpdate.as_view(), name='checkin_edit'),
    url(r'^checkins/delete/(?P<pk>\d+)$', views.CheckInDelete.as_view(), name='checkin_delete'),
]
