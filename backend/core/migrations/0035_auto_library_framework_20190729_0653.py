# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-07-29 10:53
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

def add_library_framework_page(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    try:
        site = Site.objects.get(pk=1)
    except Site.DoesNotExist:
        site = Site.objects.create(domain="app.allhere.co", name="allhere")
    
    try:
        flatpage = FlatPage.objects.get(url='/library/framework/')
        flagpage.registration_required = True
        flagpage.save()
    except FlatPage.DoesNotExist:
        flatpage = FlatPage.objects.create(
            url='/library/framework/',
            title="Library Framework",
            content="AllHere Library Strategy",
            registration_required=True,
        )
        flatpage.sites.add(site)
        flatpage.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_intervention_strategy_new_fields_20190719'),
    ]

    operations = [
        migrations.RunPython(add_library_framework_page),
    ]
