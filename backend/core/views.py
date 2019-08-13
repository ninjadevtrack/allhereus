import csv
from datetime import datetime
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed, Http404
from django.contrib.auth.forms import SetPasswordForm
from .models import CheckIn, Student, School, MyUser, Strategy, Teacher
from .forms import CheckInForm, ProfileForm, StudentForm
from xhtml2pdf import pisa
import io
from django.template import Context
from django.template.loader import get_template
from functools import cmp_to_key, reduce
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime, timedelta
from operator import or_
from .utils import download_checkins_csv
from django.contrib.humanize.templatetags.humanize import naturaltime
TABLE_DISPLAY_LIMIT = 100


def district_admin_required(login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user is a District Admin. If
    not, redirects to the log-in page unless the raise_exception parameter
    is True, in which case the PermissionDenied exception is raised.
    """
    def check_is_da(user):
        # First check if the user belongs to the group
        if user.is_district_admin:
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied("You must be a District Administrator to use this feature.")
        # As the last resort, show the login form
        return False
    return user_passes_test(check_is_da, login_url=login_url)

def teacher_required(login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user is a Teacher. If
    not, redirects to the log-in page unless the raise_exception parameter
    is True, in which case the PermissionDenied exception is raised.
    """
    def check_is_teacher(user):
        # First check if the user belongs to the group
        if user.is_teacher:
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied("You must be a Teacher to use this feature.")
        # As the last resort, show the login form
        return False
    return user_passes_test(check_is_teacher, login_url=login_url)


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

    if request.user.is_district_admin:
        checkins_url = ''
        student_roster_url = ''
        show_roster_and_checkins = False
    else:
        checkins_url = reverse('checkins')
        student_roster_url = reverse('students')
        show_roster_and_checkins = True

    context = {
        'profile_url': reverse('profile'),
        'edit_url': reverse('profile_edit'),
        'checkins_url': checkins_url,
        'student_roster_url': student_roster_url,
        'show_roster_and_checkins': show_roster_and_checkins,
        'checkin_count': request.user.checkins.count(),
        'student_roster_count': request.user.students.count(),
        'user': request.user,
        'view': 'display',
    }
    return render(request, 'core/profile.html', context)


@login_required
def profile_edit(request):
    """
    profile in editing state
    """
    profile_kwargs = {'user': request.user, 'instance':request.user}

    if request.method == 'POST':
        form = ProfileForm(request.POST, **profile_kwargs)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = ProfileForm(**profile_kwargs)
    return render(request, 'core/profile_edit.html', {
        'profile_url': reverse('profile'),
        'edit_url': reverse('profile_edit'),
        'checkin_count': request.user.checkins.count(),
        'student_roster_count': request.user.students.count(),
        'user': request.user,
        'form': form,
        'error_message': [error for error in form.non_field_errors()],
    })



@login_required
def checkins(request):
    """
    list all the checkins for teacher, school admin, district admin.
    """

    def student_sort(a, b):
        if a.name < b.name:
            return -1
        if a.name == b.name:
            return 0
        return 1

    checkins = request.user.checkins
    students = []
    for checkin in checkins:
        if checkin.student not in students:
            students.append(checkin.student)
    students.sort(key=cmp_to_key(student_sort))

    context = {'checkins': checkins, 'students': students}
    return render(request, 'core/checkins.html', context)


@login_required
def checkins_add(request):
    """
    create a new checkin
    """

    if request.method == 'GET':
        form = CheckInForm(request.user, None)
    else:
        form = CheckInForm(request.user, None, request.POST)
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
        if len(test) == 0:
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
        form = CheckInForm(request.user, None, instance=checkin)
    else:
        form = CheckInForm(request.user, None, request.POST, instance=checkin)
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
    """
    csv for view checkins:
    list all the checkins for teacher, school adminand District Admin.
    """
    student = request.GET.get('student','')
    from_date = request.GET.get('from','')
    to_date = request.GET.get('to','')
    search = request.GET.get('search', '')

    status_choices= (
            ('C', 'Completed'),
            ('U', 'Unreachable'),
            ('M', 'Left Message'),
        )
    status = [k for k, v in status_choices if search.lower() in v.lower()] + ['A']
    mode_choices=(
            ('P', 'Phone'),
            ('V', 'Visit'),
            ('I', 'In-Person'),
            ('E', 'Email')
        )
    modes = [k for k, v in mode_choices if search.lower() in v.lower()] + ['A']

    checkins = request.user.checkins \
        .filter(
            Q(teacher__first_name__icontains=search) |
            Q(teacher__last_name__icontains=search) |
            Q(student__first_name__icontains=search) |
            Q(student__first_name__icontains=search) |
            Q(student__school__name__icontains=search) |
            Q(info_learned__icontains=search) |
            Q(info_better__icontains=search) |
            reduce(or_, [Q(mode__icontains=q) for q in modes]) |
            reduce(or_, [Q(status__icontains=q) for q in status])
        )

    student_checkins = checkins
    if student != 'all':
        student_checkins = [checkin for checkin in request.user.checkins if checkin.student.name == student]

    from_date_checkins = student_checkins
    if from_date != '':
        from_date_checkins = [checkin for checkin in student_checkins if checkin.date.date() >= datetime.strptime(from_date, '%m/%d/%Y').date()]

    to_date_checkins = from_date_checkins
    if to_date != '':
        to_date_checkins = [checkin for checkin in from_date_checkins if checkin.date.date() <= datetime.strptime(to_date, '%m/%d/%Y').date()]

    return download_checkins_csv(to_date_checkins)

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = context_dict
    html  = template.render(context)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

@login_required
def checkins_pdf(request):
    """
    pdf for view checkins:
    list all the checkins for teacher or school admin.  District Admin returns 404.
    """

    student = request.GET.get('student','')
    from_date = request.GET.get('from','')
    to_date = request.GET.get('to','')
    search = request.GET.get('search', '')

    status_choices= (
            ('C', 'Completed'),
            ('U', 'Unreachable'),
            ('M', 'Left Message'),
        )
    status = [k for k, v in status_choices if search.lower() in v.lower()] + ['A']
    mode_choices=(
            ('P', 'Phone'),
            ('V', 'Visit'),
            ('I', 'In-Person'),
            ('E', 'Email')
        )
    modes = [k for k, v in mode_choices if search.lower() in v.lower()] + ['A']

    checkins = request.user.checkins \
        .filter(
            Q(teacher__first_name__icontains=search) |
            Q(teacher__last_name__icontains=search) |
            Q(student__first_name__icontains=search) |
            Q(student__first_name__icontains=search) |
            Q(student__school__name__icontains=search) |
            Q(info_learned__icontains=search) |
            Q(info_better__icontains=search) |
            reduce(or_, [Q(mode__icontains=q) for q in modes]) |
            reduce(or_, [Q(status__icontains=q) for q in status])
        )
    student_checkins = checkins
    if student != 'all':
        student_checkins = [checkin for checkin in request.user.checkins if checkin.student.name == student]

    from_date_checkins = student_checkins
    if from_date != '':
        from_date_checkins = [checkin for checkin in student_checkins if checkin.date.date() >= datetime.strptime(from_date, '%m/%d/%Y').date()]

    to_date_checkins = from_date_checkins
    if to_date != '':
        to_date_checkins = [checkin for checkin in from_date_checkins if checkin.date.date() <= datetime.strptime(to_date, '%m/%d/%Y').date()]

    return render_to_pdf(
        'core/pdf_checkins_template.html',
        {
            'pagesize':'A4',
            'checkins': to_date_checkins,
        }
    )


@login_required
def reports_in_chart(request):
    from_date = request.GET.get('from', '')
    to_date = request.GET.get('to', '')
    school_id = request.GET.get('school', 0)
    teacher_id = request.GET.get('teacher', 'all')
    student_id = request.GET.get('student', 'all')
    checkins = CheckIn.objects.filter(student__school__id=school_id)
    student_name = "All Students"
    teacher_name = "All Teachers"
    school_name = School.objects.get(pk=school_id).name

    if teacher_id != 'all':
        teacher_checkins = checkins.filter(teacher__id=teacher_id)
        teacher_name = Teacher.objects.get(pk=teacher_id).name
    else:
        teacher_checkins = checkins

    if student_id != 'all':
        student_checkins = teacher_checkins.filter(student__id=student_id)
        student_name = Student.objects.get(pk=student_id).name
    else:
        student_checkins = teacher_checkins

    from_date_checkins = student_checkins
    if from_date != '':
        from_date_checkins = student_checkins.filter(date__gte=datetime.strptime(from_date, '%m/%d/%Y').date())

    to_date_checkins = from_date_checkins
    if to_date != '':
        to_date_checkins = from_date_checkins.filter(date__lt=datetime.strptime(to_date, '%m/%d/%Y').date() + timedelta(days=1))

    intervention_type = request.GET.get('type','')
    if intervention_type == 'status':
        complete = to_date_checkins.filter(status='C').count()
        unreachable = to_date_checkins.filter(status='U').count()
        left_message = to_date_checkins.filter(status='M').count()

        return render(request, 'core/intervention_report.html', \
            { 
                'complete': complete, \
                'unreachable': unreachable, \
                'left_message': left_message, \
                'student_name': student_name, \
                'teacher_name': teacher_name, \
                'school_name': school_name,\
                'from_time':from_date, \
                'to_time': to_date
            })

    if intervention_type == 'mode':
        phone = to_date_checkins.filter(mode='P').count()
        visit = to_date_checkins.filter(mode='V').count()
        in_person = to_date_checkins.filter(mode='I').count()
        email = to_date_checkins.filter(mode='E').count()

        return render(request, 'core/intervention_report_by_format.html', \
            { 
                'phone': phone,
                'visit': visit,
                'in_person': in_person,
                'email': email,
                'student_name': student_name,
                'teacher_name': teacher_name,
                'school_name': school_name,
                'from_time':from_date, 'to_time': to_date})



    return HttpResponse("This feature is coming.")


@login_required
def student(request, id):
    """
    Display Student detail view for district_admin or Teacher.  School_admin returns 404.
    """
    if request.user.is_school_admin:
        raise Http404("This view isn't defined for School_admin.")
    student = get_object_or_404(Student, pk=id)
    return render(request, 'core/student.html', {
        'student': student,
        'recent_checkins': student.checkins[:10]
    })

@login_required
def student_edit(request, id):
    """
    Edit existing student view for district_admin or Teacher.  School_admin returns 404.
    """
    if request.user.is_school_admin:
        raise Http404("This view isn't defined for School_admin.")
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
    List view of students for district_admin or Teacher.  School_admin returns 404.
    """
    if request.user.is_school_admin:
        raise Http404("This view isn't defined for School_admin.")
    students = request.user.students.order_by('last_name')
    for student in students:
        student.teacher_checkins = student.checkins.filter(teacher=request.user).count()
    return render(request, 'core/student_list.html', {
        'students': students,
        'student_total': len(students),
    })


@login_required
def students_unassigned(request):
    """
    List view/ form to assign unassigned students to teacher for district_admin or Teacher.  School_admin returns 404.
    """
    if request.user.is_school_admin:
        raise Http404("This view isn't defined for School_admin.")
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
def student_checkin_add(request, id):
    """
    create a new checkin
    """
    student = get_object_or_404(Student, pk=id)
    form = CheckInForm(request.user, student)
    return render(request, 'core/checkin_edit.html', {
        'form': form
    })

@login_required
def students_csv(request):
    """
    csv for view students:
    list all the students for teacher or school admin.  District Admin returns 404.
    """
    if request.user.is_district_admin:
        raise Http404("This view isn't defined for District Administrators.")

    response = HttpResponse(content_type='text/csv')

    filename = f'AllHere Students Archive {datetime.now()}'
    response['Content-Disposition'] = f'attachment; filename="{ filename }.csv"'

    writer = csv.writer(response)

    writer.writerow(['First Name', 'Last Name', 'Student ID', 'Grade', 'Email',
                     'Last Check-in'])

    search = request.GET.get('search','')
    students = request.user.students.order_by('last_name') \
    .filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(student_id__icontains=search) |
            Q(grade__icontains=search) |
            Q(email__icontains=search)
        )
    for student in students:
        writer.writerow([student.first_name, student.last_name, student.student_id, student.grade, student.email, student.last_checkin.date.date()])
    return response


@login_required
def students_pdf(request):
    """
    pdf for view students:
    list all the students for teacher or school admin.  District Admin returns 404.
    """
    if request.user.is_district_admin:
        raise Http404("This view isn't defined for District Administrators.")
    response = HttpResponse(content_type='text/csv')

    filename = f'AllHere Students Archive {datetime.now()}'
    response['Content-Disposition'] = f'attachment; filename="{ filename }.csv"'

    writer = csv.writer(response)

    writer.writerow(['First Name', 'Last Name', 'Student ID', 'Grade', 'Email',
                     'Last Check-in'])

    search = request.GET.get('search','')
    students = request.user.students.order_by('last_name') \
    .filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(student_id__icontains=search) |
            Q(grade__icontains=search) |
            Q(email__icontains=search)
        )

    return render_to_pdf(
        'core/pdf_students_template.html',
        {
            'pagesize':'A4',
            'students': students,
        }
    )

@login_required
def reports(request):
    return render(request, 'core/report.html')

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


@login_required
def schools(request):
    """
    list all the schools for district_admin or school_admin.  Teacher returns 404.
    """
    if request.user.is_teacher:
        raise Http404("This view isn't defined for Teacher.")
    district = request.user.district
    schools = request.user.schools.order_by('name')
    return render(request, 'core/school_list.html', {
        'district': district,
        'schools': schools,
        'schools_total': schools.count(),
    })

@login_required
def staff(request, school_id):
    """
    List view of staff for district_admin or school_admin.  Teacher returns 404.
    """
    if request.user.is_teacher:
        raise Http404("This view isn't defined for Teacher.")
    school = get_object_or_404(request.user.schools, pk=school_id) # only allow viewing schools in my schools.
    staff = school.staff.filter(district=school.district).order_by('last_name','first_name')
    return render(request, 'core/staff_list.html', {
        'school': school,
        'staff': staff,
        'staff_total': staff.count(),
    })

@login_required
def staff_profile(request, school_id, staff_id):
    """
    Display a staff's profile for district_admin or school_admin.  Teacher returns 404.
    """
    if request.user.is_teacher:
        raise Http404("This view isn't defined for Teacher.")
    school = get_object_or_404(request.user.schools, pk=school_id) # only allow viewing schools in my schools.
    staff = get_object_or_404(school.staff, pk=staff_id)
    school_staff_kwargs = { 'school_id': school.id, 'staff_id': staff.id }
    profile_url = reverse('staff_profile', kwargs=school_staff_kwargs)
    edit_url = reverse("staff_profile_edit", kwargs=school_staff_kwargs)
    checkins_url = reverse('staff_checkins', kwargs=school_staff_kwargs)
    student_roster_url = reverse('staff_students', kwargs=school_staff_kwargs)
    show_roster_and_checkins = True,

    context = {
        'profile_url': profile_url,
        'edit_url': edit_url,
        'checkins_url': checkins_url,
        'student_roster_url': student_roster_url,
        'show_roster_and_checkins': show_roster_and_checkins,
        'checkin_count': staff.checkins.count(),
        'student_roster_count': staff.students.count(),
        'user': staff,
        'view': 'display',
    }
    return render(request, 'core/profile.html', context)

@login_required
def staff_profile_edit(request, school_id, staff_id):
    """
    staff_profile in editing state for district_admin or school_admin.  Teacher returns 404.
    """
    if request.user.is_teacher:
        raise Http404("This view isn't defined for Teacher.")
    school = get_object_or_404(request.user.schools, pk=school_id) # only allow viewing schools in my schools.
    staff = get_object_or_404(school.staff, pk=staff_id)
    staff_profile_kwargs = { 'school_id': school.id, 'staff_id': staff.id }
    profile_url = reverse('staff_profile', kwargs=staff_profile_kwargs)
    edit_url = reverse('staff_profile_edit', kwargs=staff_profile_kwargs)
    profile_kwargs = {'user': request.user, 'instance':staff}
    if request.method == 'POST':
        form = ProfileForm(request.POST, **profile_kwargs)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(profile_url)
    else:
        form = ProfileForm(**profile_kwargs)
    return render(request, 'core/profile_edit.html', {
        'profile_url': profile_url,
        'edit_url': edit_url,
        'staff_password_set_url': reverse('staff_password_set', kwargs={
            'school_id': school_id,
            'staff_id': staff_id,
        }),
        'checkin_count': staff.checkins.count(),
        'student_roster_count': staff.students.count(),
        'user': staff,
        'form': form,
        'error_message': [error for error in form.non_field_errors()],
    })

@login_required
@district_admin_required(raise_exception=True)
def staff_password_set(request, school_id, staff_id):
    """
    staff_profile in editing state
    """
    school = get_object_or_404(request.user.schools, pk=school_id) # only allow viewing schools in my schools.
    staff = get_object_or_404(school.staff, pk=staff_id) # make sure the staff is in the DA's schools
    staff_profile_kwargs = { 'school_id': school.id, 'staff_id': staff.id }
    profile_url = reverse('staff_profile', kwargs=staff_profile_kwargs)
    if not staff:
        return HttpResponseForbidden()  # Just straight up forbid this request, looking fishy already!
    if request.method == 'POST':
        form = SetPasswordForm(staff, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(profile_url)
    elif request.method == 'GET':
        form = SetPasswordForm(staff)
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
    form.fields['new_password2'].label = 'Confirm New Password'
    form.fields['new_password2'].longest = True
    return render(request, 'core/password_change.html', {
        'form': form,
        'staff': staff,
    })

@login_required
def staff_students(request, school_id, staff_id):
    """
    List view of staff students for district_admin or school_admin.  Teacher returns 404.
    """
    if request.user.is_teacher:
        raise Http404("This view isn't defined for Teacher.")
    school = get_object_or_404(request.user.schools, pk=school_id) # only allow viewing schools in my schools.
    staff = get_object_or_404(school.staff, pk=staff_id)
    students = staff.students.filter(school=school).order_by('last_name','first_name')
    return render(request, 'core/student_list.html', {
        'staff': staff,
        'students': students,
        'student_total': len(students),
    })

@login_required
def staff_student(request, school_id, staff_id, student_id):
    """
    Student details view for district_admin or school_admin.  Teacher returns 404.
    """
    if request.user.is_teacher:
        raise Http404("This view isn't defined for Teacher.")

    school = get_object_or_404(request.user.schools, pk=school_id) # only allow viewing schools in my schools.
    staff = get_object_or_404(school.staff, pk=staff_id) # make sure the staff is at the school
    student = get_object_or_404(staff.students, pk=student_id) # make sure the student belongs to staff
    return render(request, 'core/student.html', {
        'school': school,
        'staff': staff,
        'student': student,
        'recent_checkins': student.checkins[:10]
    })

@login_required
def staff_student_edit(request, school_id, staff_id, student_id):
    """
    Editing exsting student for district_admin or school_admin.  Teacher returns 404.
    """
    if request.user.is_teacher:
        raise Http404("This view isn't defined for Teacher.")
    school = get_object_or_404(request.user.schools, pk=school_id) # only allow viewing schools in my schools.
    staff = get_object_or_404(school.staff, pk=staff_id) # make sure the staff is at the school
    student = get_object_or_404(staff.students, pk=student_id) # make sure the student belongs to staff
    if request.method == 'POST':
        form = StudentForm(request.user, request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('staff_students', kwargs={
                'school_id': school_id, 'staff_id': staff_id}))
    else:
        form = StudentForm(request.user, instance=student)
    return render(request, 'core/student_edit.html', {
        'form': form,
        'view': 'edit',
        'school': school,
        'staff': staff,
        'student': student,
        'error_message': [error for error in form.non_field_errors()],
    })


@login_required
def staff_checkins(request, school_id, staff_id):
    """
    list all the checkins for district_admin or school_admin.  Teacher returns 404.
    """
    if request.user.is_teacher:
        raise Http404("This view isn't defined for Teacher.")
    school = get_object_or_404(request.user.schools, pk=school_id) # only allow viewing schools in my schools.
    staff = get_object_or_404(school.staff, pk=staff_id) # only allowing staff at the school
    checkins = staff.checkins.filter(student__school=school)

    context = {
        'checkins': checkins,
        'staff': staff,
        'school': school,
        'checkin_view': 'staff_checkin',
    }
    return render(request, 'core/checkins.html', context)

@login_required
def staff_checkin(request, school_id, staff_id, checkin_id):
    """
    view an individual checkin for district_admin or school_admin.  Teacher returns 404.
    """
    if request.user.is_teacher:
        raise Http404("This view isn't defined for Teacher.")
    school = get_object_or_404(request.user.schools, pk=school_id) # only allow viewing schools in my schools.
    staff = get_object_or_404(school.staff, pk=staff_id) # only allowing staff at the school
    checkin_event = get_object_or_404(staff.checkins, pk=checkin_id) # ensure the checkin doese in fact belong to the staff

    # 403 if user is not allowed
    has_checkin_permission(checkin_event, request.user)

    return render(request, 'core/checkin.html', {
        'checkin': checkin_event,
        'success_score_percentage': checkin_event.success_score / 10 * 100,
        'viewonly': True,
    })

@login_required
def library(request):
    """
    the landing page for Intevention Stratgy Library
    """
    context = {
        'strategies': Strategy.objects.as_of(),
        'total': len(request.user.checkins),
    }

    return render(request, 'core/library.html', context=context)

@login_required
def strategy(request, strategy_id):
    """
    the details page for an Intervention Strategy.
    """
    context = {
        'strategy': Strategy.objects.get(id=strategy_id),
    }

    return render(request, 'core/strategy.html', context=context)

@login_required
def strategies(request):
    """
    the landing page for Intevention Stratgy Library
    """
    search = request.GET.get("search", "")
    strategies = Strategy.objects.as_of()
    filtered_strategies = strategies.filter(
        Q(name__icontains=search) |
        Q(display_name__icontains=search) |
        Q(description__icontains=search) |
        Q(district__name__icontains=search) |
        Q(practice__name__icontains=search)
    )
    context = {
        'strategies': filtered_strategies.order_by('practice', 'display_name'),
        'search': search
    }

    return render(request, 'core/strategies.html', context=context)

@login_required
def schools_staff_json(request, school_id):
    teachers = Teacher.objects.filter(school__id=school_id).values('id', 'first_name', 'last_name')
    return JsonResponse(list(teachers), safe=False)

@login_required
def schools_students_json(request, school_id):
    students = Student.objects.filter(school__id=school_id).values('id', 'first_name', 'last_name')
    return JsonResponse(list(students), safe=False)

@login_required
def schools_staff_students_json(request, school_id, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    school = School.objects.get(pk=school_id)
    students = teacher.students.filter(school=school).order_by('last_name','first_name').values('id', 'first_name', 'last_name')
    return JsonResponse(list(students), safe=False)
