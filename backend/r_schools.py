from core import roster
from core.models import District, School

import logging

EDNUDGE_HOST="3.93.153.40"

def yo(text):
    print("***YO: {}".format(text))

# TODO: specify the district ID

logging.getLogger().setLevel(logging.DEBUG)
r=roster.Roster(EDNUDGE_HOST)
eschools = r.ednudge_get_schools().data

for es in eschools:
    yo(es.school_name)
    roster_action = "N"
    try:
        ahs = School.objects.get(
            ednudge_is_enabled=True,
            ednudge_school_id=es.id)
        logging.debug("Found AllHere School for EdNudge Id=%s", es.id)
    except School.DoesNotExist:
        ahs = None
        roster_action="C"
    
    if roster_action == "C":
        logging.debug("Creating AllHere School for EdNudge school_id=%s, district_id=%s", es.id, es.district_id)

        ahd = District.objects.get(ednudge_is_enabled=True, ednudge_district_id=es.district_id)

        ahs = School.objects.create(
            ednudge_is_enabled      = True,
            district                = ahd,
            ednudge_school_id       = es.id,
            ednudge_school_local_id = es.local_id,
            name                    = es.school_name         
        )

    yo("ahs: {}".format(ahs))


