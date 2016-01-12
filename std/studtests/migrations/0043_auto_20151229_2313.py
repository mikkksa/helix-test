# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studtests', '0042_auto_20151217_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=80)),
                ('visible', models.BooleanField(default=True)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2015, 12, 29, 23, 13, 8, 249000), verbose_name=b'date published')),
                ('edit_date', models.DateTimeField(default=datetime.datetime(2015, 12, 29, 23, 13, 8, 249000), verbose_name=b'date edited')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InterviewChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2015, 12, 29, 23, 13, 8, 250000), verbose_name=b'date published')),
                ('edit_date', models.DateTimeField(default=datetime.datetime(2015, 12, 29, 23, 13, 8, 250000), verbose_name=b'date edited')),
                ('interview', models.ForeignKey(to='studtests.Interview')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InterviewResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.ForeignKey(to='studtests.InterviewChoice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='question',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 29, 23, 13, 8, 242000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 29, 23, 13, 8, 242000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 29, 23, 13, 8, 240000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 29, 23, 13, 8, 240000), verbose_name=b'date published'),
            preserve_default=True,
        ),
    ]
