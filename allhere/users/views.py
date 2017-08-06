from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import UserAH, CheckIn, Team

@login_required
def dashboard(request):
    recent_checkins = CheckIn.objects.order_by('-date')[:5]
    context = {'recent_checkins': recent_checkins}
    return render(request, 'dashboard.html', context)

class UserDetailView(LoginRequiredMixin, DetailView):
    model = UserAH
    # These next two lines tell the view to index lookups by username
    slug_field = 'email'
    slug_url_kwarg = 'email'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """TODO Not sure what this does."""
    permanent = False

    def get_redirect_url(self):
        return reverse('')


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



class CheckInList(LoginRequiredMixin, ListView):
    model = CheckIn

    def get_queryset(self):
        """Returns relevant checkins for Students on teacher's teams or 
        if user is the manager, all of them for the Group"""
        if self.request.user.is_manager:
            return CheckIn.objects.filter(student__group=self.request.user.group)
        else:
            print(self.request.user.teams.count())
            return CheckIn.objects.filter(student__team__in=self.request.user.teams.all())


class CheckInCreate(LoginRequiredMixin, CreateView):
    model = CheckIn
    fields = ['date', 'teacher', 'student', 'status', 'format',
              'should_notify_school_admin', 'success_score', 'things_learned', 'how_better']
    success_url = reverse_lazy('users:checkin_list')


class CheckInUpdate(LoginRequiredMixin, UpdateView):
    model = CheckIn
    fields = ['date', 'teacher', 'student', 'status', 'format',
              'should_notify_school_admin', 'success_score', 'things_learned', 'how_better']
    success_url = reverse_lazy('users:checkin_list')


class CheckInDelete(LoginRequiredMixin, DeleteView):
    model = CheckIn
    success_url = reverse_lazy('users:checkin_list')
