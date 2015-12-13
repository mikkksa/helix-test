# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studtests', '0004_remove_student_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='tests',
            field=models.ForeignKey(choices=[(b'FR', b'Freshman'), (b'SO', b'Sophomore'), (b'JR', b'Junior'), (b'SR', b'Senior')], to='studtests.Question', null=True),
            preserve_default=True,
        ),
    ]
