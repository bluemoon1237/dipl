# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-09 14:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TuesQuestionnaireApp', '0008_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='chosen_role',
        ),
    ]
