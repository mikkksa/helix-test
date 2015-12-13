# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studtests', '0038_auto_20150607_0337'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImQuestion',
            fields=[
                ('question_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='studtests.Question')),
                ('image', models.ImageField(upload_to=b'')),
            ],
            options={
            },
            bases=('studtests.question',),
        ),
        migrations.RemoveField(
            model_name='imagetest',
            name='test_ptr',
        ),
        migrations.DeleteModel(
            name='ImageTest',
        ),
        migrations.AlterField(
            model_name='question',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 8, 11, 24, 58, 251000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 8, 11, 24, 58, 251000), verbose_name=b'date published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='edit_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 8, 11, 24, 58, 250000), verbose_name=b'date edited'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 8, 11, 24, 58, 250000), verbose_name=b'date published'),
            preserve_default=True,
        ),
    ]
