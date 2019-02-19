from core import roster
from core.models import District, School, Section

import logging

EDNUDGE_HOST="3.93.153.40"

def yo(text):
    print("***YO: {}".format(text))

# TODO: specify the district ID

logging.getLogger().setLevel(logging.DEBUG)
r=roster.Roster(EDNUDGE_HOST)
esections = r.ednudge_get_sections('d:39761370-c5bb-41e8-88a3-10d6d21ffbd7').data

for es in esections:
    yo("school_id:{}, section_id".format(es.school_id, es.id))
    roster_action="N"
    try:
        ahs = Section.objects.get(
            ednudge_is_enabled=True,
            ednudge_section_id=es.id)
        logging.debug("Found AllHere Section for EdNudge Id=%s", es.id)
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

    yo("ahs: {}".format(ahs))


