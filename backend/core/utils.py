import csv
from django.http import HttpResponse
from datetime import datetime

def download_checkins_csv(queryset):
    response = HttpResponse(content_type='text/csv')

    filename = f'AllHere Checkins Archive {datetime.now()}'
    response['Content-Disposition'] = f'attachment; filename="{ filename }.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'teacher', 'Student', 'Status', 'Format',
                    'Info learned', 'Info better', 'Success score'])

    for checkin in queryset:
        writer.writerow([checkin.date, checkin.teacher, checkin.student,
                    checkin.get_status_display(), checkin.get_mode_display(),
                    checkin.info_learned, checkin.info_better,
                    checkin.success_score])
    return response

def download_users_csv(queryset):
    response = HttpResponse(content_type='text/csv')

    filename = f'AllHere Users Archive {datetime.now()}'
    response['Content-Disposition'] = f'attachment; filename="{ filename }.csv"'
    writer = csv.writer(response)
    writer.writerow(['Email', 'First_name', 'Last_name', 'Department', 'Role', 'IsManager', 'IsActive',
                    'IsStaff', 'District', 'School', 'Grade', 'Subject', 'Date Joined', 'Last Updated', ])

    for user in queryset:
        writer.writerow([user.email, user.first_name, user.last_name,
                    user.department, user.get_role_display(),
                    user.is_manager, user.is_active, user.is_staff, user.district,
                    user.school, user.grade, user.subject, user.date_joined,
                    user.last_updated])
    return response