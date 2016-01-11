# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import bank.terminal.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CardUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('number', models.CharField(unique=True, max_length=16, validators=[django.core.validators.RegexValidator('\\d{16}', 'Number must be of length 16 and must consist only of numbers')])),
                ('balance', models.IntegerField()),
                ('is_blocked', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', bank.terminal.models.CardUserManager()),
            ],
        ),
    ]
