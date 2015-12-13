# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studtests', '0007_student_tests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='school',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='tests',
            field=models.ManyToManyField(to='studtests.Teacher'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='teacher',
            name='school',
            field=models.ForeignKey(to='studtests.School', null=True),
            preserve_default=True,
        ),
    ]
