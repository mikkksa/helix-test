from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import studtests.models as stmodels
import scorm_api.models as scmodels
import scorm_api
import uuid
from resources import lrs_properties
from tincan import (
    RemoteLRS,
    Statement,
    Agent,
    Verb,
    Activity,
    Context,
    LanguageMap,
    ActivityDefinition,
    StateDocument,
)


def index(request):
    if request.POST:
        form = scmodels.UploadFile(request.POST, request.FILES)
        if form.is_valid:
            file = request.FILES['file']
            file_ = scmodels.UploadedTinCan(file=file)
            file_.save()
        return redirect("/scorm/")
    else:
        form = stmodels.UploadFileForm()
    return render(request, "scorm_api/index.html",
                  {"username": request.session["username"], "usertype": request.session['usertype'], 'form': form})
