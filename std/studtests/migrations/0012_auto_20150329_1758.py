# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studtests', '0011_question_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='school',
            field=models.ForeignKey(to='studtests.School'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='login',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='school',
            field=models.ForeignKey(to='studtests.School', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='surname',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
