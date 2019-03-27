from core import roster
from core.models import District, School, Student, StudentDailyAttendance
import os
import logging


EDNUDGE_HOST=os.getenv('EDNUDGE_API_URL')
EDNUDGE_USERNAME=os.getenv('EDNUDGE_USERNAME')
EDNUDGE_PASSWORD=os.getenv('EDNUDGE_PASSWORD')

logging.getLogger().setLevel(logging.DEBUG)

def yo(text):
    print("***YO: {}".format(text))

class RAttendance:

    def r_attendance(self, district_id):
        r=roster.Roster(EDNUDGE_HOST, EDNUDGE_USERNAME, EDNUDGE_PASSWORD)
        eattendance = r.ednudge_get_dailyattendance(district_id).data
        for ea in eattendance:
            yo("dailyattendance_id:{}".format(ea.id))
            roster_action="N"
            try:
                aa = StudentDailyAttendance.objects.get(
                    ednudge_is_enabled=True,
                    ednudge_dailyattendance_id=ea.id)
                logging.debug("Found AllHere StudentDailyAttendance for EdNudge Id=%s", ea.id)

                if aa.ednudge_merkleroot == ea.merkleroot:
                    roster_action = "N"
                else:
                    roster_action = "U"
            except StudentDailyAttendance.DoesNotExist:
                aa = None
                roster_action="C"
            
            if roster_action == "C":
                logging.debug("Creating AllHere StudentDailyAttendance for EdNudge id=%s", ea.id)

                #TODO: ahd = District.objects.get(ednudge_is_enabled=True, ednudge_district_id=ea.district_id)
                ahschool = School.objects.get(ednudge_is_enabled=True, ednudge_school_id=ea.school_id)
                ahs = Student.objects.get(ednudge_is_enabled=True, ednudge_learner_id=ea.learner_id)
                
                aa = StudentDailyAttendance.objects.create(
                    ednudge_is_enabled      = True,
                    school                  = ahschool,
                    student                 = ahs,
                    date                    = ea.attendance_date,
                    mark                    = ea.mark[0].lower(),
                    ednudge_dailyattendance_id       = ea.id,
                    ednudge_dailyattendance_local_id = ea.local_id,
                    ednudge_merkleroot      = ea.id,
                )

            if roster_action == "U":
                logging.debug("Updating AllHere StudentDailyAttendance for EdNudge id=%s", ea.id)
                aa.mark                = ea.mark[0].lower()
                aa.ednudge_merkleroot  = ea.id
                aa.save(update_fields=['mark','ednudge_merkleroot'])

            yo("aa: {}".format(aa))


if __name__ == '__main__':
    district_id = District.objects.get(ednudge_district_local_id='8888').ednudge_district_id
    yo("i'm main!")
    rs = RAttendance()
    rs.r_attendance(district_id)

yo("__name__={}".format(__name__))

district_id = District.objects.get(ednudge_district_local_id='8888').ednudge_district_id
yo("i'm main!")
rs = RAttendance()
rs.r_attendance(district_id)