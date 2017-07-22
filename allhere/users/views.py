from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import UserAH


class UserDetailView(LoginRequiredMixin, DetailView):
    model = UserAH
    # These next two lines tell the view to index lookups by username
    slug_field = 'email'
    slug_url_kwarg = 'email'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'pk': self.request.user.id})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', 'school', 'position', 'grade', 'content_area']

    # we already imported User in the view code above, remember?
    model = UserAH

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'pk': self.request.user.id})

    def get_object(self):
        # Only get the User record for the user making the request
        return UserAH.objects.get(pk=self.request.user.id)


class UserListView(LoginRequiredMixin, ListView):
    model = UserAH
    # These next two lines tell the view to index lookups by username
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
