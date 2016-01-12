# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studtests', '0043_auto_20151229_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewresult',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interview',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 30, 19, 32, 54, 535000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interview',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 30, 19, 32, 54, 535000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interviewchoice',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 30, 19, 32, 54, 536000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interviewchoice',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 30, 19, 32, 54, 535000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 30, 19, 32, 54, 528000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 30, 19, 32, 54, 528000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 30, 19, 32, 54, 526000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 30, 19, 32, 54, 526000), verbose_name=b'date published'),
            preserve_default=True,
        ),
    ]
