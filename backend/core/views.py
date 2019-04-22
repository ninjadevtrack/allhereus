import csv
from datetime import datetime
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from .models import CheckIn, Student
from .forms import CheckInForm, ProfileForm, StudentForm
from xhtml2pdf import pisa
import io
from django.template import Context
from django.template.loader import get_template
from functools import cmp_to_key, reduce
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime, timedelta
from operator import or_

from django.contrib.humanize.templatetags.humanize import naturaltime
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
    response = HttpResponse(content_type='text/csv')

    filename = f'AllHere Checkins Archive {datetime.now()}'
    response['Content-Disposition'] = f'attachment; filename="{ filename }.csv"'

    writer = csv.writer(response)

    writer.writerow(['Date', 'teacher', 'Student', 'Status', 'Format',
                     'Info learned', 'Info better', 'Success score'])
                     
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


    for checkin in to_date_checkins:
        writer.writerow([checkin.date, checkin.teacher, checkin.student,
                         checkin.get_status_display(), checkin.get_mode_display(),
                         checkin.info_learned, checkin.info_better,
                         checkin.success_score])

    return response

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
    checkins = request.user.checkins
    from_date = request.GET.get('from', '')
    to_date = request.GET.get('to', '')
    student = request.GET.get('student', 'all')
    student_name = "All Students"

    intervention_type = request.GET.get('type','')
    if student != 'all':
        checkins = request.user.checkins.filter(student__id=student)
        student_name = Student.objects.get(pk=student).name
    from_date_checkins = checkins
    if from_date != '':
        from_date_checkins = checkins.filter(date__gte=datetime.strptime(from_date, '%m/%d/%Y').date())

    to_date_checkins = from_date_checkins
    if to_date != '':
        to_date_checkins = from_date_checkins.filter(date__lt=datetime.strptime(to_date, '%m/%d/%Y').date() + timedelta(days=1))

    if intervention_type == 'status':
        complete = to_date_checkins.filter(status='C').count()
        unreachable = to_date_checkins.filter(status='U').count()
        left_message = to_date_checkins.filter(status='M').count()

        return render(request, 'core/intervention_report.html', \
            { 'complete': complete, 'unreachable': unreachable, 'left_message': left_message, \
            'student_name': student_name, 'from_time':from_date, 'to_time': to_date})

    if intervention_type == 'score':
        scores = [0] * 10
        for i in range(10):
            scores[i] = to_date_checkins.filter(success_score=i).count()
        return render(request, 'core/intervention_report_by_score.html', \
            { 'scores' : scores, 'student_name': student_name, 'from_time':from_date, 'to_time': to_date })

    if intervention_type == 'mode':
        phone = to_date_checkins.filter(mode='P').count()
        visit = to_date_checkins.filter(mode='V').count()
        in_person = to_date_checkins.filter(mode='I').count()
        email = to_date_checkins.filter(mode='E').count()

        return render(request, 'core/intervention_report_by_format.html', \
            { 'phone': phone, 'visit': visit, 'in_person': in_person, 'email': email, \
            'student_name': student_name, 'from_time':from_date, 'to_time': to_date})

        

    return HttpResponse("This feature is coming.")


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
@user_passes_test(lambda u: u.is_superuser)
def reports(request):
    """
    displays report
    """
    students = Student.objects.all().only("id", "first_name", "last_name")
    return render(request, 'core/report.html', {"students": students})

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
