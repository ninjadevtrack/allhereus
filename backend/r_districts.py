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
from core.models import District
import os
import logging

EDNUDGE_HOST=os.getenv('EDNUDGE_API_URL')
EDNUDGE_USERNAME=os.getenv('EDNUDGE_USERNAME')
EDNUDGE_PASSWORD=os.getenv('EDNUDGE_PASSWORD')


def yo(text):
    print("***YO: {}".format(text))

logging.getLogger().setLevel(logging.DEBUG)
r=roster.Roster(EDNUDGE_HOST, EDNUDGE_USERNAME, EDNUDGE_PASSWORD)
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
