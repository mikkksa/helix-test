# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studtests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='teacher',
            field=models.ForeignKey(to='studtests.Teacher', null=True),
            preserve_default=True,
        ),
    ]
