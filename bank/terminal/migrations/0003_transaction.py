# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0002_carduser_wrong_tries'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('operation', models.CharField(max_length=2, choices=[('WD', 'Withdraw money'), ('CB', 'Check balance')])),
                ('date', models.DateTimeField(auto_now=True)),
                ('amount', models.PositiveIntegerField(blank=True)),
                ('card', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
