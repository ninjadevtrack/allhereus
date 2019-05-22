import os, sys

proj_path = "/var/app/"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from core import roster
from core.models import District, School, Student
import os
import logging


EDNUDGE_HOST=os.getenv('EDNUDGE_API_URL')
EDNUDGE_USERNAME=os.getenv('EDNUDGE_USERNAME')
EDNUDGE_PASSWORD=os.getenv('EDNUDGE_PASSWORD')

logging.getLogger().setLevel(logging.DEBUG)

def yo(text):
    print("***YO: {}".format(text))

class RGuardians:

    def r_guardians(self, district_id):
        r=roster.Roster(EDNUDGE_HOST, EDNUDGE_USERNAME, EDNUDGE_PASSWORD)
        eguardians = r.ednudge_get_guardians(district_id).data
        for eg in eguardians:
            yo("guardian_id:{}".format(eg.id))

            # for each learner, update their parent contact info
            for elearner in eg.learners:
                logging.debug(f"guardian learner_id: {elearner.learner_id}, relationship_type: {elearner.relationship_type}")

                try:
                    astudent = Student.objects.get(
                        ednudge_is_enabled = True,
                        ednudge_learner_id = elearner.learner_id)
                    logging.debug(f"AllHere Student found: {astudent.id}")
                except Student.DoesNotExist:
                    logging.debug(f"AllHere Student missing: {astudent.id}")
                    astudent = None

                if astudent and elearner.relationship_type.lower() == "parent":
                    astudent.parent_first_name = eg.first_name
                    astudent.parent_last_name = eg.last_name
                    astudent.parent_email = eg.email
                    astudent.phone = eg.sms
                    astudent.save(update_fields=['parent_first_name', 'parent_last_name', 'parent_email', 'phone'])
                    logging.debug(f"Updated student_id={astudent.id} with guadian_id={eg.id}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} $district_local_id")
        sys.exit()
    else:
        district_local_id = sys.argv[1]

    district_id = District.objects.get(ednudge_district_local_id='8888').ednudge_district_id
    yo("i'm main!")
    rs = RGuardians()
    rs.r_guardians(district_id)

yo("__name__={}".format(__name__))

district_id = District.objects.get(ednudge_district_local_id='8888').ednudge_district_id
yo("i'm main!")
rs = RGuardians()
rs.r_guardians(district_id)
