# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carduser',
            name='wrong_tries',
            field=models.IntegerField(default=0),
        ),
    ]
