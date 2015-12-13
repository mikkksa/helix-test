# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studtests', '0034_auto_20150531_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='answers_count',
            field=models.CharField(max_length=3, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 31, 15, 19, 46, 144000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 31, 15, 19, 46, 144000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 31, 15, 19, 46, 143000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 31, 15, 19, 46, 143000), verbose_name=b'date published'),
            preserve_default=True,
        ),
    ]
