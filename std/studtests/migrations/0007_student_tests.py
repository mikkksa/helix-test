# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studtests', '0006_remove_student_tests'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='tests',
            field=models.ManyToManyField(to='studtests.Question'),
            preserve_default=True,
        ),
    ]
