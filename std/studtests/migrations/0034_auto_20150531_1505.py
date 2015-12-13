# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studtests', '0033_auto_20150521_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='right_count',
            field=models.CharField(max_length=3, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='testresult',
            name='unright_count',
            field=models.CharField(max_length=3, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 31, 15, 5, 0, 588000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 31, 15, 5, 0, 588000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 31, 15, 5, 0, 587000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 31, 15, 5, 0, 587000), verbose_name=b'date published'),
            preserve_default=True,
        ),
    ]
