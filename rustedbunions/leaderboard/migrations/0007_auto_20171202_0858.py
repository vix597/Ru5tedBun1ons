# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-02 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0006_auto_20171202_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaderboardentry',
            name='leader_oid',
            field=models.CharField(default='65c3e74b77014c1a8ec5d3d6eb8649f8', max_length=32, verbose_name='Leader OID'),
        ),
    ]
