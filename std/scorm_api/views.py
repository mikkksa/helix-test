from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import studtests.models as stmodels
import scorm_api.models as scmodels
import json
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
            file_ = scmodels.UploadedTinCan(file=file, user=User.objects.get(username=request.session['username']))
            file_.save()
            working(file_)
        return redirect("/scorm/")
    else:
        form = stmodels.UploadFileForm()
    return render(request, "scorm_api/index.html",
                  {"username": request.session["username"], "usertype": request.session['usertype'], 'form': form})


def working(file):
    f = open(file.file.path, 'r+')
    fr = f.read()
    parsed_string = json.loads(fr)
    kek = parsed_string['verb']['id']
    return 0


def create_test(paths, request, test):
    for x in paths:
        f = open(x, 'r+')
        fr = f.read()
        parsed = json.loads(fr)
        if parsed['verb']['id'] == 'http://adlnet.gov/expapi/verbs/answered':
            teacher = stmodels.Teacher.objects.get(login=request.session['username'])
            def_ = parsed['object']['definition']
            desc = def_['description']['en-US']
            question = stmodels.Question(question_text=desc,
                                         subject=stmodels.Subject.objects.get(subject=request.session['sub'],
                                                                              school=teacher.school),
                                         teacher=teacher, school=teacher.school, grade=stmodels.Grade.objects.get(grade=request.session['grade']))
            if def_['interactionType'] == "choice":
                question.enter = False
                question.test = test
                question.save()
                choices = def_['choices']
                corrects = str(def_['correctResponsesPattern'])[3:len(str(def_['correctResponsesPattern']))-2].split('[,]')
                for y in choices:
                    choice = stmodels.Choice(choice_text=y['id'], question=question)
                    if choice.choice_text in corrects:
                        choice.right_choice = True
                    choice.save()
    return 0


def myfiles(request):
    teacher = stmodels.Teacher.objects.get(login=request.session['username'])
    subs = [x for x in stmodels.Subject.objects.all() if
            x.school.id == stmodels.Teacher.objects.get(login=request.session['username']).school.id]
    grades = stmodels.Grade.objects.all()
    args = {"username": request.session['username'], 'usertype': request.session['usertype'], 'subs': subs,
            'grades': grades}
    tns = [x for x in scmodels.UploadedTinCan.objects.all() if
           x.user == User.objects.get(username=request.session['username'])]
    files = []
    for x in tns:
        files.append(x.file)
    args['files'] = files
    if request.POST:
        if "create" in request.POST:
            sub = request.POST.get('sub')
            request.session['sub'] = sub
            request.session['grade'] = request.POST.get('grade')
            files_checked = [x.replace('c_', '') for x in request.POST if x.startswith('c_')]
            test = stmodels.Test(name=request.POST.get('name'),
                                 subject=stmodels.Subject.objects.get(subject=request.session['sub'],
                                                                      school=teacher.school),
                                 teacher=teacher, school=teacher.school, grade=stmodels.Grade.objects.get(grade=request.session['grade']))
            test.save()
            create_test(files_checked, request, test)
            return HttpResponseRedirect('/scorm/myfiles/')
    return render(request, "scorm_api/myfiles.html", args)
