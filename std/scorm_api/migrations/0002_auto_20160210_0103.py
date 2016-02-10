# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorm_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedtincan',
            name='file',
            field=models.FileField(null=True, upload_to=b'scorm_api/files'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='uploadedtincan',
            name='name',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
