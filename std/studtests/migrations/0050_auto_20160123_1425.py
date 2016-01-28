# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studtests', '0049_auto_20160122_0242'),
    ]

    operations = [

        migrations.AddField(
            model_name='question',
            name='enter',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interview',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 23, 14, 25, 50, 561000), verbose_name='date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interview',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 23, 14, 25, 50, 561000), verbose_name='date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interviewchoice',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 23, 14, 25, 50, 562000), verbose_name='date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interviewchoice',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 23, 14, 25, 50, 562000), verbose_name='date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 23, 14, 25, 50, 554000), verbose_name='date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 23, 14, 25, 50, 554000), verbose_name='date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 23, 14, 25, 50, 551000), verbose_name='date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 23, 14, 25, 50, 551000), verbose_name='date published'),
            preserve_default=True,
        ),
    ]
