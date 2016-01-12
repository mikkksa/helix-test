# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studtests', '0045_auto_20160102_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewchoice',
            name='pick',
            field=models.CharField(max_length=5, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interview',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 10, 15, 896000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interview',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 10, 15, 896000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interviewchoice',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 10, 15, 897000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interviewchoice',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 10, 15, 897000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 10, 15, 889000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 10, 15, 889000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 10, 15, 887000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 17, 10, 15, 887000), verbose_name=b'date published'),
            preserve_default=True,
        ),
    ]
