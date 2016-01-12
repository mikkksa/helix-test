# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studtests', '0041_auto_20151217_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 17, 39, 43, 948000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='grade',
            field=models.ForeignKey(to='studtests.Grade', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 17, 39, 43, 948000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='school',
            field=models.ForeignKey(to='studtests.School', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(to='studtests.Subject', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 17, 39, 43, 946000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 17, 39, 43, 946000), verbose_name=b'date published'),
            preserve_default=True,
        ),
    ]
