# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-08 18:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TuesQuestionnaireApp', '0005_auto_20170108_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttemptAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TuesQuestionnaireApp.Attempt')),
                ('real_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TuesQuestionnaireApp.Answer')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
