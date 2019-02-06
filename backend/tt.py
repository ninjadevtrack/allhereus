from core import roster

import logging

EDNUDGE_HOST="5b2f1a37.ngrok.io"

logging.getLogger().setLevel(logging.DEBUG)
r=roster.Roster(EDNUDGE_HOST)
r.get_districts()
