# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-20 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, verbose_name='Username')),
                ('password', models.CharField(max_length=100, verbose_name='password')),
                ('security_question', models.CharField(max_length=1000, verbose_name='Security Question')),
                ('security_answer', models.CharField(max_length=100, verbose_name='Security Answer')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]