# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-16 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventManager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='teacherPassword',
            field=models.CharField(default='anits123*', max_length=25),
        ),
    ]