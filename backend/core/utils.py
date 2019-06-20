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