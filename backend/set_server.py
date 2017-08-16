from django.contrib.sites.models import Site
my_site = Site.objects.get(pk=1)
my_site.domain = 'platform.allhere.com'
my_site.name = 'AllHere'
my_site.save()
