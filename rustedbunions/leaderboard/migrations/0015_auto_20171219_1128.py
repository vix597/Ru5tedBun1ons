# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-19 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0014_auto_20171219_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaderboardentry',
            name='leader_oid',
            field=models.CharField(default='0999a5b8e5a349ac8a61b8a0f1e04d20', max_length=32, verbose_name='Leader OID'),
        ),
    ]
