# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-01 03:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventManager', '0002_auto_20160716_1931'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adminName', models.CharField(max_length=100)),
                ('adminPassword', models.CharField(max_length=25)),
            ],
        ),
    ]