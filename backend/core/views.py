from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """
    the homepage of the user
    """

    username = 'Aldo Raine'
    recent_checkins = [{
        'id': 1,
        'student': 'Hans Zimmer',
        'teacher': 'Joe Shmoe',
        'time': datetime.now()
    }, {
        'id': 2,
        'student': 'Chris Nolan',
        'teacher': 'Joe Shmoe',
        'time': datetime.now()
    }]

    context = {'username': username, 'recent_checkins': recent_checkins}
    return render(request, 'core/home.html', context=context)


def login(request):
    """
    used for logging in with an existing account
    """
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def signup(request):
    """
    used for signing up for the platform
    """
    return render(request, 'core/signup.html')


def forgotpassword(request):
    """
    view to enable sending password reset email
    """
    return render(request, 'core/forgotpassword.html')

@login_required
def profile(request):
    """
    displays user's info
    """
    return render(request, 'core/profile.html')

@login_required
def profile_edit(request):
    """
    profile in editing state
    """
    return render(request, 'core/profile_edit.html')

@login_required
def checkins(request):
    """
    list all the checkins for teacher
    """
    return render(request, 'core/checkins.html')

@login_required
def checkins_add(request):
    """
    create a new checkin
    """
    return render(request, 'core/checkins_add.html')

@login_required
def checkin(request, id):
    """
    view an individual checkin
    """
    return render(request, 'core/checkin.html')

@login_required
def checkin_edit(request, id):
    """
    edit an individual checkin
    """
    return render(request, 'core/checkin_edit.html')

@login_required
def teams(request):
    """
    Teacher: list of teams that the user is currently on
    Manager: list of all teams of the manager's group
    """
    return render(request, 'core/teams.html')

@login_required
def team(request, id):
    """
    view individual team
    """
    return render(request, 'core/team.html')
