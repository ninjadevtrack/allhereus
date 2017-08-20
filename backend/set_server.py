import logging

from django.contrib.sites.models import Site

logger = logging.getLogger(__name__)
logger.info('Setting server name')

my_site = Site.objects.get(pk=1)
my_site.domain = 'app.allhere.com'
my_site.name = 'AllHere'
my_site.save()
