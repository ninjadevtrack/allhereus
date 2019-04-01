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
from core.models import District, School, Section

import os
import logging

EDNUDGE_HOST=os.getenv('EDNUDGE_API_URL')
EDNUDGE_USERNAME=os.getenv('EDNUDGE_USERNAME')
EDNUDGE_PASSWORD=os.getenv('EDNUDGE_PASSWORD')

logging.getLogger().setLevel(logging.DEBUG)

def yo(text):
    print("***YO: {}".format(text))

class RSections:

    def r_sections(self, district_id):
        r=roster.Roster(EDNUDGE_HOST, EDNUDGE_USERNAME, EDNUDGE_PASSWORD)
        esections = r.ednudge_get_sections(district_id).data
        for es in esections:
            yo("school_id:{}, section_id".format(es.school_id, es.id))
            roster_action="N"
            try:
                ahs = Section.objects.get(
                    ednudge_is_enabled=True,
                    ednudge_section_id=es.id)
                logging.debug("Found AllHere Section for EdNudge Id=%s", es.id)

                if ahs.ednudge_merkleroot == es.merkleroot:
                    roster_action = "N"
                else:
                    roster_action = "U"
            except Section.DoesNotExist:
                ahs = None
                roster_action="C"
            
            if roster_action == "C":
                logging.debug("Creating AllHere Section for EdNudge section_id=%s, district_id=%s", es.id, es.district_id)

                ahd = District.objects.get(ednudge_is_enabled=True, ednudge_district_id=es.district_id)
                ahschool = School.objects.get(ednudge_is_enabled=True, ednudge_school_id=es.school_id)

                ahs = Section.objects.create(
                    ednudge_is_enabled      = True,
                    district                = ahd,
                    school                  = ahschool,
                    ednudge_section_id       = es.id,
                    ednudge_section_local_id = es.local_id,
                    name                    = es.section_name,
                    term_name               = es.term_name,
                    term_start_date         = es.term_start_date[0:10],
                    term_end_date           = es.term_end_date[0:10],
                    period                  = es.period,
                    subject                 = es.subject
                )

            if roster_action == "U":
                logging.debug("Updating AllHere Section for EdNudge section_id=%s, district_id=%s", es.id, es.district_id)
                ahs.name                    = es.section_name
                ahs.term_name               = es.term_name
                ahs.term_start_date         = es.term_start_date[0:10]
                ahs.term_end_date           = es.term_end_date[0:10]
                ahs.period                  = es.period
                ahs.subject                 = es.subject
                ahs.ednudge_merkleroot      = es.merkleroot
                ahs.save(update_fields=['name','term_name',
                    'term_start_date','term_end_date','period',
                    'subject','ednudge_merkleroot'])



            yo("ahs: {}".format(ahs))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} $district_local_id")
        sys.exit()
    else:
        district_local_id = sys.argv[1]

    district_id = District.objects.get(ednudge_district_local_id=district_local_id).ednudge_district_id
    yo("i'm main!")
    rs = RSections()
    rs.r_sections(district_id)

yo("__name__={}".format(__name__))
district_id = District.objects.get(ednudge_district_local_id='8888').ednudge_district_id
yo("i'm main!")
rs = RSections()
rs.r_sections(district_id)