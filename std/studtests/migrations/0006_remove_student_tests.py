# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studtests', '0005_student_tests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='tests',
        ),
    ]
