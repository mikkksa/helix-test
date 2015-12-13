# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studtests', '0010_student_tests'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='school',
            field=models.ForeignKey(to='studtests.School', null=True),
            preserve_default=True,
        ),
    ]
