# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studtests', '0048_auto_20160108_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('definition', models.CharField(max_length=2000)),
                ('image', models.ImageField(upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),

        migrations.AlterField(
            model_name='interview',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 2, 42, 44, 292000), verbose_name='date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interview',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 2, 42, 44, 292000), verbose_name='date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interviewchoice',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 2, 42, 44, 293000), verbose_name='date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interviewchoice',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 2, 42, 44, 293000), verbose_name='date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 2, 42, 44, 284000), verbose_name='date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 2, 42, 44, 284000), verbose_name='date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 2, 42, 44, 281000), verbose_name='date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 2, 42, 44, 281000), verbose_name='date published'),
            preserve_default=True,
        ),
    ]
