from django.db import models
from django.forms import forms
from grab.tools.encoding import smart_unicode


class UploadFile(forms.Form):
    file = forms.FileField()


class UploadedTinCan(models.Model):
    file = models.FileField(upload_to="/scorm_api/files", null=True)
    name = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return smart_unicode(self.name)
