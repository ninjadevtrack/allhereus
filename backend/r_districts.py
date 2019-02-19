from core import roster
from core.models import District

import logging

EDNUDGE_HOST="3.93.153.40"

def yo(text):
    print("***YO: {}".format(text))

logging.getLogger().setLevel(logging.DEBUG)
r=roster.Roster(EDNUDGE_HOST)
edistricts = r.ednudge_get_districts().data

for ed in edistricts:
    yo(ed.name)
    roster_action="N"
    try:
        ahd = District.objects.get(
            ednudge_is_enabled=True,
            ednudge_district_id=ed.id)
        logging.debug("Found AllHere District for EdNudge Id=%s", ed.id)
    except District.DoesNotExist:
        ahd = None
        roster_action="C"


    if roster_action == "C":
        logging.debug("Creating AllHere District for EdNudge District ID=%s", ed.id)
        ahd = District.objects.create(
            ednudge_is_enabled  = True,
            ednudge_district_id = ed.id,
            ednudge_district_local_id    = ed.local_id,
            name                = ed.name         
        )

    #yo("ahd: {}".format(ahd))
