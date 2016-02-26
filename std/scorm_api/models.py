from django.db import models
from django.forms import forms
from grab.tools.encoding import smart_unicode
from django.contrib.auth.models import User


class UploadFile(forms.Form):
    file = forms.FileField()

    def __unicode__(self):
        return smart_unicode(self.file)


class UploadedTinCan(models.Model):
    user = models.ForeignKey(User, null=True)
    file = models.FileField(upload_to="scorm_api", null=True)
    name = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return smart_unicode(self.name) or u''
