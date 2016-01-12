# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studtests', '0046_auto_20160102_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 11, 46, 2000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interview',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 11, 46, 2000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interviewchoice',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 11, 46, 4000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interviewchoice',
            name='pick',
            field=models.CharField(default=0, max_length=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interviewchoice',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 11, 46, 4000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 11, 45, 977000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 11, 45, 977000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 11, 45, 967000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 11, 45, 967000), verbose_name=b'date published'),
            preserve_default=True,
        ),
    ]
