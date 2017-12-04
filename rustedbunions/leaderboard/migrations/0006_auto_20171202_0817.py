# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-02 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0005_auto_20171202_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaderboardentry',
            name='display_name',
            field=models.CharField(default='', max_length=25, verbose_name='Display Name'),
        ),
        migrations.AlterField(
            model_name='leaderboardentry',
            name='leader_oid',
            field=models.CharField(default='f034405ebc914fe8836c6d06371ac77f', max_length=32, verbose_name='Leader OID'),
        ),
    ]