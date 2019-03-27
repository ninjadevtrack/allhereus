from core import roster
from core.models import District, School

import logging

EDNUDGE_HOST="18.221.122.128"

def yo(text):
    print("***YO: {}".format(text))

# TODO: specify the district ID

logging.getLogger().setLevel(logging.DEBUG)
r=roster.Roster(EDNUDGE_HOST)

district_id = District.objects.get(ednudge_district_local_id='8888').ednudge_district_id

eschools = r.ednudge_get_schools(district_id).data

for es in eschools:
    yo(es.school_name)
    roster_action = "N"
    try:
        ahs = School.objects.get(
            ednudge_is_enabled=True,
            ednudge_school_id=es.id)
        logging.debug("Found AllHere School for EdNudge Id=%s", es.id)

        if ahs.ednudge_merkleroot == es.merkleroot:
            roster_action = "N"
        else:
            roster_action = "U"
        
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
            name                    = es.school_name,
            ednudge_merkleroot      = es.merkleroot        
        )

    if roster_action == "U":
        logging.debug("Updating AllHere School for EdNudge school_id=%s, district_id=%s", es.id, es.district_id)
        ahs.name = es.school_name
        ahs.ednudge_merkleroot = es.merkleroot
        ahs.save(update_fields=['name', 'ednudge_merkleroot'])

    yo("ahs: {}".format(ahs))


