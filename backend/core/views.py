import csv
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from .models import CheckIn, Student
from .forms import CheckInForm, ProfileForm, StudentForm

TABLE_DISPLAY_LIMIT = 100


@login_required
def home(request):
    """
    the homepage of the user
    """
    context = {
        'recent_checkins': request.user.checkins[:10],
        'total': len(request.user.checkins),
    }

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
    context = {
        'recent_checkins': request.user.checkins[:10],
        'user': request.user,
        'view': 'display',
    }
    return render(request, 'core/profile.html', context)


@login_required
def profile_edit(request):
    """
    profile in editing state
    """

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'core/profile_edit.html', {
        'recent_checkins': request.user.checkins[:10],
        'form': form,
        'error_message': [error for error in form.non_field_errors()],
    })


@login_required
def checkins(request):
    """
    list all the checkins for teacher
    """

    context = {'checkins': request.user.checkins}
    return render(request, 'core/checkins.html', context)


@login_required
def checkins_add(request):
    """
    create a new checkin
    """

    if request.method == 'GET':
        form = CheckInForm(request.user)
    else:
        form = CheckInForm(request.user, request.POST)
        # If data is valid, proceeds to create a new CheckIn and redirect the user
        if form.is_valid():
            form.save()
            return redirect('checkins')

    return render(request, 'core/checkin_edit.html', {
        'form': form,
        'error_message': [error for error in form.non_field_errors()],
    })


# Throw PermissionDenied Exception if user does not have permission to view
def has_checkin_permission(checkin, user):
    if checkin.district != user.district:
        raise PermissionDenied("Checkin is not in your district")
    if checkin.school != user.school and not user.is_district_admin:
        raise PermissionDenied("Checkin is not in your school")
    if checkin.teacher != user and not user.is_school_admin and not user.is_district_admin:
        test = user.students.filter(id=checkin.student.id)
        if test == None:
            raise PermissionDenied("Checkin is not in yours")


@login_required
def checkin(request, id):
    """
    view an individual checkin
    """
    checkin_event = get_object_or_404(CheckIn, pk=id)

    # 403 if user is not allowed
    has_checkin_permission(checkin_event, request.user)

    return render(request, 'core/checkin.html', {
        'checkin': checkin_event,
        'success_score_percentage': checkin_event.success_score / 10 * 100,
    })


@login_required
def checkin_edit(request, id):
    """
    edit an individual checkin
    """

    checkin = get_object_or_404(CheckIn, pk=id)

    # 403 if user is not allowed
    has_checkin_permission(checkin, request.user)

    if request.method == 'GET':
        form = CheckInForm(request.user, instance=checkin)
    else:
        form = CheckInForm(request.user, request.POST, instance=checkin)
        if form.is_valid():
            form.save()
            return redirect('checkins')

    return render(request, 'core/checkin_edit.html', {
        'checkin': checkin,
        'form': form,
        'error_message': [error for error in form.non_field_errors()],
    })


@login_required
def checkin_delete(request, id):
    """
    Delete an individual checkin
    """
    checkin = get_object_or_404(CheckIn, pk=id)

    # 403 if user is not allowed
    has_checkin_permission(checkin, request.user)

    if request.method == 'POST':
        checkin.delete()
        return redirect('checkins')

    return render(request, 'core/checkin_delete.html', {'checkin': checkin})


@login_required
def checkins_csv(request):
    response = HttpResponse(content_type='text/csv')

    filename = f'AllHere Checkins Archive {datetime.now()}'
    response['Content-Disposition'] = f'attachment; filename="{ filename }.csv"'

    writer = csv.writer(response)

    writer.writerow(['date', 'teacher', 'student', 'status', 'visit type',
                     'info learned', 'info better', 'success score'])

    checkins = request.user.checkins
    for checkin in checkins:
        writer.writerow([checkin.date, checkin.teacher, checkin.student,
                         checkin.get_status_display(), checkin.get_mode_display(),
                         checkin.info_learned, checkin.info_better,
                         checkin.success_score])

    return response


@login_required
def student(request, id):
    """
    Student detail view
    """
    student = get_object_or_404(Student, pk=id)
    return render(request, 'core/student.html', {
        'student': student,
        'recent_checkins': student.checkins[:10]
    })


@login_required
def student_add(request):
    """
    Create new student
    """
    if request.method == 'POST':
        form = StudentForm(request.user, request.POST)
        form.district = request.user.district
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students'))
    else:
        form = StudentForm(request.user)
    return render(request, 'core/student_edit.html', {
        'form': form,
        'error_message': [error for error in form.non_field_errors()],
    })


@login_required
def student_edit(request, id):
    """
    Edit existing student
    """
    student = get_object_or_404(Student, pk=id)
    if request.method == 'POST':
        form = StudentForm(request.user, request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students'))
    else:
        form = StudentForm(request.user, instance=student)
    return render(request, 'core/student_edit.html', {
        'form': form,
        'view': 'edit',
        'student': student,
        'error_message': [error for error in form.non_field_errors()],
    })


@login_required
def students(request):
    """
    List view of students
    """
    students = request.user.students.order_by('last_name')
    return render(request, 'core/student_list.html', {
        'students': students,
        'student_total': len(students),
    })


@login_required
def students_unassigned(request):
    """
    List view/ form to assign unassigned students to teacher
    """
    errors = []
    if request.method == 'POST':
        student_ids = []
        for form_input in request.POST:
            # get primary key values from checkboxes with name formated 'checkbox-<pk>'
            if form_input.split('-')[0] == 'checkbox':
                student_ids.append(int(form_input.split('-')[1]))
        students = []
        for student_id in student_ids:
            try:
                student = Student.objects.get(pk=student_id)
                if student.teacher:
                    errors.append(f'Student already has a teacher assigned')
                students.append(student)
            except ObjectDoesNotExist:
                errors.append(f'Student does not exist for provided id')
        if not errors:
            for student in students:
                student.teacher = request.user
                student.save()
            return HttpResponseRedirect(reverse('students'))
    students = request.user.unassigned_students
    return render(request, 'core/students_unassigned.html', {'students': students, 'error_message': errors})


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


def privacy(request):
    """
    return the privacy policy
    """
    return render(request, 'core/privacy.html')


def support(request):
    """
    return the support page
    """
    return render(request, 'core/support.html')
