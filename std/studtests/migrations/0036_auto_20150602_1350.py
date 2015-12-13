# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studtests', '0035_auto_20150531_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeTest',
            fields=[
                ('test_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='studtests.Test')),
                ('time', models.CharField(max_length=3)),
            ],
            options={
            },
            bases=('studtests.test',),
        ),
        migrations.AlterField(
            model_name='question',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 2, 13, 50, 31, 80000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 2, 13, 50, 31, 80000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 2, 13, 50, 31, 80000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 2, 13, 50, 31, 80000), verbose_name=b'date published'),
            preserve_default=True,
        ),
    ]
