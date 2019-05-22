# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-04-03 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_student_total_absences'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='deleted_on',
            field=models.DateTimeField(blank=True, db_column='deleted_on', help_text='Soft delete timestamp - The date and time when the record was soft deleted.  This should be empty when is_deleted is False.', null=True),
        ),
        migrations.AddField(
            model_name='district',
            name='is_deleted',
            field=models.BooleanField(db_column='is_deleted', default=False, help_text='Soft delete indicator flag - When true the record is no longer visible on the front end though data is retained in case it was deleted my mistake.'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='deleted_on',
            field=models.DateTimeField(blank=True, db_column='deleted_on', help_text='Soft delete timestamp - The date and time when the record was soft deleted.  This should be empty when is_deleted is False.', null=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='is_deleted',
            field=models.BooleanField(db_column='is_deleted', default=False, help_text='Soft delete indicator flag - When true the record is no longer visible on the front end though data is retained in case it was deleted my mistake.'),
        ),
        migrations.AddField(
            model_name='school',
            name='deleted_on',
            field=models.DateTimeField(blank=True, db_column='deleted_on', help_text='Soft delete timestamp - The date and time when the record was soft deleted.  This should be empty when is_deleted is False.', null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='is_deleted',
            field=models.BooleanField(db_column='is_deleted', default=False, help_text='Soft delete indicator flag - When true the record is no longer visible on the front end though data is retained in case it was deleted my mistake.'),
        ),
        migrations.AddField(
            model_name='section',
            name='deleted_on',
            field=models.DateTimeField(blank=True, db_column='deleted_on', help_text='Soft delete timestamp - The date and time when the record was soft deleted.  This should be empty when is_deleted is False.', null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='is_deleted',
            field=models.BooleanField(db_column='is_deleted', default=False, help_text='Soft delete indicator flag - When true the record is no longer visible on the front end though data is retained in case it was deleted my mistake.'),
        ),
        migrations.AddField(
            model_name='sectionstudent',
            name='deleted_on',
            field=models.DateTimeField(blank=True, db_column='deleted_on', help_text='Soft delete timestamp - The date and time when the record was soft deleted.  This should be empty when is_deleted is False.', null=True),
        ),
        migrations.AddField(
            model_name='sectionstudent',
            name='is_deleted',
            field=models.BooleanField(db_column='is_deleted', default=False, help_text='Soft delete indicator flag - When true the record is no longer visible on the front end though data is retained in case it was deleted my mistake.'),
        ),
        migrations.AddField(
            model_name='sectionteacher',
            name='deleted_on',
            field=models.DateTimeField(blank=True, db_column='deleted_on', help_text='Soft delete timestamp - The date and time when the record was soft deleted.  This should be empty when is_deleted is False.', null=True),
        ),
        migrations.AddField(
            model_name='sectionteacher',
            name='is_deleted',
            field=models.BooleanField(db_column='is_deleted', default=False, help_text='Soft delete indicator flag - When true the record is no longer visible on the front end though data is retained in case it was deleted my mistake.'),
        ),
        migrations.AddField(
            model_name='student',
            name='deleted_on',
            field=models.DateTimeField(blank=True, db_column='deleted_on', help_text='Soft delete timestamp - The date and time when the record was soft deleted.  This should be empty when is_deleted is False.', null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='is_deleted',
            field=models.BooleanField(db_column='is_deleted', default=False, help_text='Soft delete indicator flag - When true the record is no longer visible on the front end though data is retained in case it was deleted my mistake.'),
        ),
    ]
