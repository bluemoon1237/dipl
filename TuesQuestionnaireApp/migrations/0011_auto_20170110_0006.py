# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-09 22:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('TuesQuestionnaireApp', '0010_assignment_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='time_limit',
            field=models.IntegerField(default=0, verbose_name='Time limit(in minutes)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attempt',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='attempt',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='participants',
            field=models.ManyToManyField(related_name='attending_courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
