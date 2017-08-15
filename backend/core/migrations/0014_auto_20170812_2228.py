# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-12 22:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20170812_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='status',
            field=models.CharField(choices=[('I', 'In Progress'), ('C', 'Completed'), ('U', 'Unreachable'), ('M', 'Left Message')], default='I', help_text='Current status of check-in.', max_length=1),
        ),
    ]