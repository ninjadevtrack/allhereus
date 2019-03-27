from core.models import District, School, Section

import logging

logging.getLogger().setLevel(logging.DEBUG)

def yo(text):
    print("***YO: {}".format(text))

sections = Section.objects.filter(ednudge_is_enabled=True)
yo(sections)
sections.delete()
yo(sections)

ss = School.objects.filter(ednudge_is_enabled=True)
yo(ss)
ss.delete()
yo(ss)

dd = District.objects.filter(ednudge_is_enabled=True)
yo(dd)
dd.delete()
yo(dd)

