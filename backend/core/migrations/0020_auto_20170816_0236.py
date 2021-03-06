# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 02:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20170814_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='language',
            field=models.CharField(blank=True, help_text="Student/family's spoken language.", max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(blank=True, help_text='School identifier for student.', max_length=255, null=True, verbose_name='Student ID'),
        ),
    ]
