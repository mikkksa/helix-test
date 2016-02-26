# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scorm_api', '0002_auto_20160210_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedtincan',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uploadedtincan',
            name='file',
            field=models.FileField(null=True, upload_to=b'scorm_api'),
            preserve_default=True,
        ),
    ]
