# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random, time, threading

from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.models import User

from  studtests.models import Question, Teacher, Subject, Choice, Test, Student, TestResult, Grade, TimeTest, \
    ImQuestion, UploadFileForm, RndTest, Interview, InterviewChoice, InterviewResult

from django.contrib.sessions.backends.db import SessionStore


def logined(request):
    if 'username' in request.session and 'usertype' in request.session:
        return [request.session['username'], request.session['usertype']]
    else:
        return None


"""Index page"""


def index(request):
    if not 'username' in request.session:
        return render(request, 'studtests/First.html')
    latest_question_list = Question.objects.all()
    context = {'latest_question_list': latest_question_list}
    if 'username' in request.session:
        context['username'] = request.session['username']
    if 'usertype' in request.session:
        context['usertype'] = request.session['usertype']
    return render(request, 'studtests/index.html', context)


"""Random questions"""


def RndQuestions(questionlist, count):
    return random.sample(questionlist, int(count))


"""Tests where subject = chosen subject"""


def subject_test(request, subject_id):
    tests = []
    subject = Subject.objects.get(id=int(subject_id))
    student = Student()
    if 'usertype' in request.session:
        if request.session['usertype'] == "s":
            student = Student.objects.get(login=request.session['username'])
    for test in Test.objects.all():
        finished = False
        for tr in TestResult.objects.all():
            if tr.test.name == test.name and tr.student == student:
                finished = True

        if test.subject == subject and test.visibility and test.school == subject.school and not finished:
            tests.append(test)
    context = {'tests': tests}
    if 'username' in request.session:
        context['username'] = request.session['username']
    if 'usertype' in request.session:
        context['usertype'] = request.session['usertype']
    return render(request, 'studtests/subject_test.html', context)


"""Subjects where school == student school"""


def subjects(request):
    user = Student()
    if 'username' in request.session and request.session['usertype'] == "s":
        user = Student.objects.get(login=request.session['username'])
    subs = Subject.objects.all()
    subjects = []
    for sub in subs:
        if sub.school == user.school:
            subjects.append(sub)
    context = {'subjects': subjects}
    if 'username' in request.session:
        context['username'] = request.session['username']
    if 'usertype' in request.session:
        context['usertype'] = request.session['usertype']
    return render(request, 'studtests/subjects.html', context)


"""Here is test's questions and choices for them"""


def detail(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    timetest = TimeTest()
    questions = Question.objects.all()
    choices = Choice.objects.all()
    context = {'test': test, 'questions': questions}
    imquests = ImQuestion.objects.all()
    type = ""
    began = 0
    timetec = 0

    """If test already done"""
    for x in TestResult.objects.all():
        if x.test.id == test.id and x.student.id == Student.objects.get(login=logined(request)[0]).id:
            return redirect('/')
    for x in TimeTest.objects.all():
        if x.name == test.name:
            type = "time"
            timetest = x
            test = x
            break
    for x in RndTest.objects.all():
        if x.name == test.name:
            type = "rnd"
            test = x
            qs = x.question_set.all()
            questions = RndQuestions(qs, x.qcount)
            break
    if request.POST:
        return HttpResponse("kek")
    if 'starts' in request.session and request.session['starts'] is not None:
        began = Test.objects.get(pk=int(request.session['starts'])).id
        if 'timestart' in request.session:
            timetec = int(timetest.time) - (int(time.time() - request.session['timestart']))
    if 'username' in request.session:
        context = {'test': test, 'username': request.session['username'], 'questions': questions, 'choices': choices,
                   'type': type, 'usertype': request.session['usertype'], 'test1': timetest, 'imqusests': imquests,
                   'began': began, 'timeost': timetec}
        if 'bot' in request.POST:
            context['timer'] = 'begin'
    return render(request, 'studtests/detail.html', context)


"""for result string"""


def results(request, question_id):
    response = "You're looking at the results of question %s."
    question = Question.objects.get(id=question_id)
    if "ch" in request.session:
        if request.session["ch"]:
            response += "True"
    return HttpResponse(response % question_id)


"""True/False"""


def vote(request, test_id):
    p = get_object_or_404(Test, pk=test_id)
    student = Student.objects.get(login=request.session['username'])
    finished = False
    for t in TestResult.objects.all():
        if t.test == p and t.student == student:
            finished = True
    if not finished:
        checkbox_list = [x for x in request.POST if x.startswith('choice')]
        list = []
        a = 0
        right_choices = []
        unright_choices = []
        selected_choices = []
        """get all choices with correct question"""
        for c in checkbox_list:
            id = c.replace('choice_', '')
            selected_choice = Choice.objects.get(id=int(id))
            if selected_choice.right_choice:
                list += 'True'
                a += 1
                right_choices.append(selected_choice)
            else:
                list += 'False'
                unright_choices.append(selected_choice)
        s = Student.objects.get(login=request.session['username'])
        tr = TestResult(student=s, test=p, balls=0, quest_count=len(p.question_set.all()))
        if (p in RndTest.objects.all()):
            rtest = RndTest.objects.get(name=p.name)
            tr = TestResult(student=s, test=p, balls=0, quest_count=rtest.qcount)
        tr.save()
        right_count = 0
        unright_count = 0
        choicecount = 0
        for x in tr.test.question_set.all():
            choicecount += len(x.choice_set.all())
        for x in right_choices:
            tr.right_choices.add(x)
            right_count += 1
        for x in unright_choices:
            tr.unright_choices.add(x)
            unright_count += 1
        tr.right_count = right_count
        tr.unright_count = unright_count
        tr.answers_count = choicecount
        tr.save()
        if a == len(checkbox_list):
            s.question_list.add(p)
        request.session['starts'] = None

        return redirect('/')
    else:
        raise Http404("You've already finished this test")


"""Creating Test and Questions for it"""


def create(request):
    context = {}
    user = Teacher()
    grades = Grade.objects.all()
    question_list = [x for x in request.POST if x.startswith('choice')]

    if 'usertype' in request.session and 'username' in request.session:
        if request.session['usertype'] == "s":
            context = {'username': request.session['username'], 'usertype': "s"}
        elif request.session['usertype'] == "t" and 'username' in request.session:
            user = Teacher.objects.get(login=request.session['username'])
            subs = [x for x in Subject.objects.all() if x.school == user.school]
            if 'questions' in request.session:
                context = {'username': request.session['username'], 'usertype': "t",
                           'count': len(request.session['questions']),
                           'sublist': subs, 'grades': grades, 'inputs': 4}
            else:
                context = {'username': request.session['username'], 'usertype': "t", 'sublist': subs, 'grades': grades,
                           'inputs': "123"}

    if request.POST.get("create_question"):
        question = Question(question_text=request.POST.get("question_text"),
                            grade=Grade.objects.get(grade=request.session['grade']),
                            school=user.school, teacher=user, test=Test.objects.get(name=request.session['testname']),
                            theme=request.session['theme'], visibility=True,
                            subject=Subject.objects.get(subject=request.session['sub']))
        formup = UploadFileForm(request.POST, request.FILES)
        if formup.is_valid:
            try:
                file = request.FILES['file']
                question = ImQuestion(question_text=request.POST.get("question_text"),
                                      grade=Grade.objects.get(grade=request.session['grade']),
                                      school=user.school, teacher=user,
                                      test=Test.objects.get(name=request.session['testname']),
                                      theme=request.session['theme'], visibility=True,
                                      subject=Subject.objects.get(subject=request.session['sub']), image=file)
            except:
                pass
        question.save()
        test = Test.objects.get(name=request.session['testname'])
        sessionlist = request.session['questions']
        sessionlist.append(question.id)
        request.session['questions'] = sessionlist
        right_choices = 0
        for c in question_list:
            id = c.replace('choice_', '')
            box = "id" + id
            if box in request.POST:
                choice = Choice(choice_text=request.POST[str(c)], question=question, right_choice=True)
                right_choices += 1
            else:
                if request.POST.get('choice_' + id).replace(" ", "") == "":
                    continue
                else:
                    choice = Choice(choice_text=request.POST[str(c)], question=question, right_choice=False)
            choice.save()
        test.choice_count = right_choices + request.session['c_count']
        request.session['c_count'] += right_choices
        test.save()
        context = {'username': request.session['username'], 'usertype': "t", 'count': len(request.session['questions']),
                   'formup': formup}
        return render(request, "studtests/create_question.html", context)

    if request.POST.get("end"):
        # rndq = RndQuestions(request.session['questions'], 3)
        return render(request, "studtests/index.html",
                      {"username": request.session['username'], 'usertype': request.session['usertype']})

    if request.POST.get("usualtest"):
        context["testtype"] = "usual"
        return render(request, "studtests/create_test.html", context)
    if request.POST.get("timetest"):
        context["testtype"] = "time"
        request.session['type'] = "time"
        return render(request, "studtests/create_test.html", context)
    if request.POST.get("rndtest"):
        context["testtype"] = "rnd"
        request.session['type'] = "rnd"
        return render(request, "studtests/create_test.html", context)

    if request.POST.get("create_test"):
        request.session['c_count'] = 0
        request.session['questions'] = []
        nametest = request.POST.get("test_name")
        grade = request.POST.get("test_grade")
        theme = request.POST.get("test_theme")
        sub = request.POST.get("sel")
        request.session['testname'] = nametest
        request.session['grade'] = str(grade)
        request.session['theme'] = theme
        request.session['sub'] = str(sub)
        if "time" in request.POST:
            time = request.POST.get("time")
            test = TimeTest(name=nametest, grade=Grade.objects.get(grade=grade), theme=theme,
                            subject=Subject.objects.get(subject=sub),
                            school=user.school, visibility=True, teacher=user, time=time)
            test.save()
        elif "rnd" in request.POST:
            qucount = request.POST.get("rnd")
            test = RndTest(name=nametest, grade=Grade.objects.get(grade=grade), theme=theme,
                           subject=Subject.objects.get(subject=sub),
                           school=user.school, visibility=True, teacher=user, qcount=qucount)
            test.save()
        else:
            test = Test(name=nametest, grade=Grade.objects.get(grade=grade), theme=theme,
                        subject=Subject.objects.get(subject=sub),
                        school=user.school, visibility=True, teacher=user)
            test.save()
        formup = UploadFileForm(request.POST, request.FILES)
        context['formup'] = formup
        return render(request, "studtests/create_question.html", context)

    return render(request, "studtests/create_test.html", context)


"""For teachers"""


def test_res(request, res):
    student = Student()
    testres = TestResult.objects.get(id=res)
    right = testres.right_choices
    unright = testres.unright_choices
    if 'usertype' in request.session and 'username' in request.session:
        if request.session['usertype'] == "s":
            raise Http404('Go away, student')
        if request.session['usertype'] == "t":
            student = Student.objects.get(login=testres.student.login)
            context = {'username': request.session['username'], 'usertype': "t", 'right': right.all(),
                       'unright': unright.all()}
            return render(request, "studtests/testresult.html", context)
    return HttpResponse('Test result with id: ' + str(res) + ' and student: ' + student.login + str(right))


"""For students"""


def lookresults(request):
    results = TestResult.objects.all()
    ress = []
    context = {}
    if 'usertype' in request.session and 'username' in request.session:
        if request.session['usertype'] == "s":
            user = Student.objects.get(login=request.session['username'])
            for res in results:
                if res.student == user:
                    ress.append(res)
            context = {'username': request.session['username'], 'usertype': "s", 'results': ress}
        elif request.session['usertype'] == "t" and 'username' in request.session:
            context = {'username': request.session['username']}
            raise Http404("Yo're a teacher")
    return render(request, "studtests/studresults.html", context)


"""For students"""


def lookresult(request, testres_id):
    context = {}
    p = TestResult.objects.get(pk=testres_id)
    try:
        user = Student.objects.get(login=request.session['username'])
    except:
        raise Http404("You do not have permissions")
    if p.student == user:
        right_choices = p.right_choices
        unright_choices = p.unright_choices
        if 'usertype' in request.session and 'username' in request.session:
            if request.session['usertype'] == "s":
                context = {'username': request.session['username'], 'usertype': "s", 'right': right_choices.all(),
                           'unright': unright_choices.all()}
            elif request.session['usertype'] == "t":
                raise Http404("You're teacher, mothefucker")
    else:
        raise Http404("Permission denied")
    return render(request, "studtests/testresult.html", context)


"""All teacher's students"""


def students(request):
    students_ = []
    context = {}
    if 'usertype' in request.session and 'username' in request.session:
        if request.session['usertype'] == 't':
            user = Teacher.objects.get(login=request.session['username'])
            for st in Student.objects.all():
                if st.school == user.school:
                    students_.append(st)
            context = {'username': request.session['username'], 'usertype': request.session['usertype'],
                       'students': students_}
    return render(request, 'studtests/students.html', context)


"""All tests for one teacher"""


def all_tests(request):
    tests = []
    context = {}
    testtype = ''
    raited = False
    classes = Grade.objects.all()
    for x in TimeTest.objects.all():
        f = 0
    if 'usertype' in request.session and 'username' in request.session:
        if request.session['usertype'] == 't':
            user = Teacher.objects.get(login=request.session['username'])
            for test in TestResult.objects.all():
                if test.test.school == user.school and test.test.teacher == user:
                    if 'cl' in request.POST:
                        if test.student.grade.grade == request.POST.get('cl'):
                            tests.append(test)
                    else:
                        tests.append(test)
                    if test.balls != 0:
                        raited = test.balls
            if request.POST and not 'cl' in request.POST:
                balls = [x for x in request.POST if x.startswith('rat')]
                edballs = [x for x in request.POST if x.startswith('ed')]
                edrats = [x for x in request.POST if x.startswith('eeds') and request.POST[x]]
                entrats = [x for x in request.POST if x.startswith('ents') and request.POST[x]]
                if len(balls) > 0 and len(entrats) > 0:
                    tr = TestResult.objects.get(pk=int(entrats[0].replace('ents', '')))
                    ball = 0
                    for i, x in enumerate(balls):
                        if int(entrats[0].replace('ents', '')) == int(x.replace('rat', '')):
                            ball = i
                    tr.balls = request.POST.get(balls[ball])
                    tr.save()
                if len(edballs) > 0 and len(edrats) > 0:
                    edtr = TestResult.objects.get(pk=int(edrats[0].replace('eeds', '')))
                    edball = 0
                    for i, x in enumerate(edballs):
                        if edrats[0].replace('eeds', '') == x.replace('ed', '') or x[len(x) - 1] == 'c':
                            edball = i
                    edtr.balls = request.POST.get(edballs[edball])
                    edtr.save()
                return redirect('/tests/')
            context = {'username': request.session['username'], 'usertype': 't', 'tests': tests, 'raiting': raited,
                       'classes': classes}
    return render(request, 'studtests/all_tests.html', context)


"""User's profile"""


def profile(request):
    args = {}
    args['username'] = request.session['username']
    args['usertype'] = request.session['usertype']
    if args['usertype'] == 't':
        user = Teacher.objects.get(login=args['username'])
        args['tests'] = Test.objects.filter(teacher=user)
    else:
        user = Student.objects.get(login=args['username'])
        trs = []
        for x in TestResult.objects.all():
            trs.append(x.test)
        args['tests'] = [x for x in Test.objects.all() if x not in trs]
    args['user'] = user
    return render(request, 'studtests/profile.html', args)


"""All student results"""


def student_results(request, student_id):
    context = {}
    trs = []
    if 'username' in request.session and 'usertype' in request.session:
        if request.session['usertype'] == "t":
            student = Student.objects.get(id=student_id)
            for tr in TestResult.objects.all():
                if tr.student == student:
                    trs.append(tr)
            context = {'usertype': "t", 'username': request.session['username'], 'trs': trs}
    return render(request, 'studtests/student_results.html', context)


"""Teacher's tests and managing them"""


def teachertests(request):
    tests = []
    if 'usertype' in request.session and request.session['usertype'] == "t":
        teacher = Teacher.objects.get(login=request.session['username'])
        tests = Test.objects.filter(teacher=teacher)
        context = {'username': request.session['username'], 'usertype': 't', 'tests': tests}
        setf = [x for x in request.POST if x.startswith("setf")]
        if request.POST.get('apply') or len(setf) > 0:
            dels_ = [x for x in request.POST if x.startswith("del")]
            viss_ = [x for x in request.POST if x.startswith('vis')]
            sts_ = [x for x in request.POST if x.startswith("st")]
            for a in viss_:
                test_id = a.replace('vis', '')
                test = Test.objects.get(id=test_id)
                test.visibility = True
                test.save()
            for a in sts_:
                test_id = a.replace('st', '')
                test = Test.objects.get(id=test_id)
                test.visibility = False
                test.save()
            for a in dels_:
                test_id = a.replace('del', '')
                test = Test.objects.get(id=test_id)
                test.delete()
            for a in setf:
                test_id = a.replace('setf', '')
                test = Test.objects.get(pk=int(test_id))
                undone = []
                completests = []
                for x in TestResult.objects.all():
                    if x.test == test:
                        completests.append(x.student)
                for x in Student.objects.all():
                    if x not in completests and x.grade == test.grade and x.school == test.school:
                        undone.append(x)
                for x in undone:
                    testres = TestResult(student=x, test=test, balls=2, quest_count=len(test.question_set.all()),
                                         right_count=0, unright_count=0,
                                         answers_count=len(
                                             Choice.objects.filter(question=Question.objects.get(test=test))))
                    testres.save()
        return render(request, 'studtests/created tests.html', context)
    else:
        raise Http404('Access denied')


"""Looking a test"""


def teachertest(request, test_id):
    test = Test.objects.get(id=test_id)
    questions = test.question_set.all()
    choices = Choice.objects.all()
    return render(request, "studtests/tdetail.html",
                  {'username': request.session['username'], 'usertype': request.session['usertype'],
                   'questions': questions, 'choices': choices, 'test': test})


"""Show all apis"""


def apis(request):
    try:
        return render(request, 'studtests/apis.html',
                      {'username': request.session['username'], 'usertype': request.session['usertype']})
    except:
        return render(request, 'studtests/apis.html')


"""Info page"""


def info(request):
    try:
        return render(request, 'studtests/info.html',
                      {'username': request.session['username'], 'usertype': request.session['usertype']})
    except:
        return render(request, 'studtests/info.html')


"""Getting path for question image. Commentaries aren't deleted for not forgetting the method"""


def image(request, path):
    path = 'studtests/images/' + path
    """Imtest = ImageTest.objects.get(id=3)
    im = Imtest.image.path
    im = im[24:]
    """
    """return  render(request, 'studtests/getimg.html', {'path':path, 'username':request.session['username']})
    a = ImageTest.objects.get(id = 1)
    image = ImageTest.objects.get(image=path)

    image_data = open(path, "rb").read()"""
    context = {'username': request.session['username'], 'usertype': request.session['usertype'], 'path': path}
    # return HttpResponse(image_data, content_type="image/png")
    return render(request, 'studtests/getimg.html', context)


def raitings(request):
    student = Student.objects.get(login=request.session['username'])
    trs = TestResult.objects.filter(student=student)
    return render(request, 'studtests/raitings.html',
                  {'trs': trs, 'username': request.session['username'], 'usertype': request.session['usertype']})


"""Getting information from android device and sending callback"""


@csrf_exempt
def gettrfromandr(request):
    data = []
    if request.POST:
        if request.POST.get('login') and request.POST.get('password'):
            print 'login and pass found'
            user = auth.authenticate(username=request.POST.get('login'), password=request.POST.get('password'))
            auth.login(request, user)
            for t in Teacher.objects.all():
                if t.login == request.POST.get('login'):
                    data = ['1', 't', t.id]
            for s in Student.objects.all():
                if s.login == request.POST.get('login'):
                    data = ['1', 's', s.id]
        elif request.POST.get('testresults'):
            print 'te'
            questions = []
            choices = []
            rightq = []
            falseq = []
            anddata = request.POST.get('testresults')
            data = anddata.split('/')
            studname = data[0]
            student = Student.objects.get(login=studname)
            testid = data[1]
            test = Test.objects.get(pk=int(testid))
            for i, x in enumerate(data[2:len(data) - 1]):
                if i % 2 == 0:
                    questions.append(x)
                else:
                    choices.append(x)
            for i, x in enumerate(questions):
                question = Question.objects.get(question_text=x)
                if question.test == test:
                    choices_ = Choice.objects.filter(question=question)
                    for j, y in enumerate(choices_):
                        for k in choices:
                            if y.right_choice and k[j] == '1':
                                rightq.append(y)
                            elif not y.right_choice and k[j] == '1':
                                falseq.append(y)
            try:
                tr = TestResult(student=student, test=test, balls=0,
                                quest_count=len(Question.objects.filter(test=test)),
                                unright_count=len(falseq),
                                right_count=len(rightq))
                tr.save()
                choicecount = 0
                for x in tr.test.question_set.all():
                    choicecount += len(x.choice_set.all())
                for x in rightq:
                    tr.right_choices.add(x)
                for x in falseq:
                    tr.unright_choices.add(x)
                tr.answers_count = choicecount
                tr.save()
            except Exception:
                print Exception
            print 'right: ' + str(rightq)
            print 'false' + str(falseq)
            print request.POST.get('testresults')
        elif request.POST.get('delete'):
            test = Test.objects.get(pk=int(request.POST.get('delete')))
            test.clean()
        elif request.POST.get('getav'):
            print request.POST.get('getav')
            student = Student.objects.get(login=request.POST.get('getav'))
            tested = False
            strtests = ""
            tests = Test.objects.all()
            for x in tests:
                for tr in TestResult.objects.all():
                    if tr.test == x and tr.student == student:
                        tested = True
                if not tested:
                    strtests += str(x.id) + "/"
                tested = False
            print "finished"
            return HttpResponse(strtests)
        elif request.POST.get('gettresults'):
            trs = []
            teacher = Teacher.objects.get(pk=int(request.POST.get('gettresults')))
            for x in TestResult.objects.all():
                if x.test.teacher == teacher:
                    trs.append(x.id)
            strtrs = ""
            for x in trs:
                strtrs += x + "/"
            return HttpResponse(strtrs)
        elif request.POST.get('gettestinfo'):
            test = Test.objects.get(pk=int(request.POST.get('getquestions')))
            return test.theme + "/" + test.school + "/" + test.grade
        elif request.POST.get('getquestions'):
            test = Test.objects.get(pk=int(request.POST.get('getquestions')))
            strqu = ""
            for x in Question.objects.filter(test=test):
                strqu += x.id + "/"
            return HttpResponse(strqu)
        elif request.POST.get('getchoices'):
            question = Question.objects.get(pk=int(request.POST.get('getchoices')))
            strch = ""
            for x in Choice.objects.filter(question=question):
                strch += x.id + "/"
            return HttpResponse(strch)
        elif request.POST.get('ttests'):
            teacher = Teacher.objects.get(pk=int(request.POST.get('ttests')))
            strtests = ""
            for x in Test.objects.filter(teacher=teacher):
                strtests += x.id + "/"
            return HttpResponse(strtests)
    return HttpResponse(data)


"""Ajax technology for menu with subjects"""


def ajresp(request):
    subs = []
    ids = []
    if logined(request)[1] == "s":
        subs = [str(x.subject) for x in Subject.objects.all() if
                x.school == Student.objects.get(login=logined(request)[0]).school]
        ids = [str(x.id) for x in Subject.objects.all() if
               x.school == Student.objects.get(login=logined(request)[0]).school]
    strsubs = ""
    for i, x in enumerate(subs):
        strsubs += x + ',' + ids[i] + ','
    return HttpResponse(strsubs)


def timecount(request):
    tested = False
    student = Student.objects.get(login=request.session['username'])
    a = int(str(request.session['starts']))
    test = Test.objects.get(pk=a)
    request.session['starts'] = None
    request.session.modified = True
    request.session.save()
    for x in TestResult.objects.all():
        if x.test.id == a and x.student.id == student.id:
            tested = True
    if not tested:
        tr = TestResult(student=student, test=test, balls=2)
        tr.save()
    print a
    print 'ok'


@csrf_exempt
def timestat(request):
    if 'time' in request.POST:
        request.session['starts'] = None
        id = int(request.POST['time'])
        test = TimeTest.objects.get(pk=id)
        t = threading.Timer(int(test.time), timecount, [request])
        if not 'starts' in request.session:
            a = [int(request.POST['test'])]
            request.session['starts'] = a
        else:
            a = request.session['starts']
            if not int(request.POST['time']) in request.POST:
                a = (int(request.POST['time']))
                request.session['starts'] = a
        t.start()
        request.session['timestart'] = time.time()
        """Else test already beganned and student has some problems"""
    """if 'tmes' in request.POST:
        if 'tmes' in request.POST:
        tid = int(request.POST['id'])
        test = TimeTest.objects.get(pk=tid)"""

    return HttpResponse("kek")


def createinterview(request):
    if request.session['usertype'] == "t":
        if request.POST:
            name = request.POST.get("name")
            group = request.POST.get("group")
            interview = Interview(name=name, group=group, user=User.objects.get(username=request.session['username']))
            interview.save()
            choices = [x for x in request.POST if x.startswith("ch")]
            for x in choices:
                choice = InterviewChoice(interview=interview, name=request.POST.get(x))
                choice.save()
            return redirect("/")
    return render(request, 'studtests/createint.html',
                  {'username': request.session['username'], 'usertype': request.session['usertype']})


def find_interview(request):
    context = {'username': request.session['username'], 'usertype': request.session['usertype']}
    if request.POST:
        if "send" in request.POST:
            choices_ = [x for x in request.POST if x.startswith("r")]
            choices__ = []
            for x in choices_:
                choice = InterviewChoice.objects.get(pk=int(request.POST[x]))
                choice.pick = str(int(choice.pick) + 1)
                choice.save()
                choices__.append(request.POST.get(x))
                intresult = InterviewResult(user=User.objects.get(username=request.session['username']),
                                            choice=choice)
                intresult.save()
            return redirect("/")
        else:
            group = request.POST.get("intertext")
            interviews, choices = [], []
            checked = False
            for x in Interview.objects.all():
                for y in InterviewResult.objects.all():
                    if y.user == User.objects.get(username=request.session['username']) and y.choice.interview == x:
                        checked = True
                if x.group == group and x.visible and not checked:
                    interviews.append(x)
                    choices.append(x.interviewchoice_set)
                checked = False
            context["interviews"], context["choices"] = interviews, choices
    return render(request, "studtests/detail_int.html", context)


def detail_interviews(request):
    args = {"username": request.session['username'], "usertype": request.session['usertype']}
    interviews = [x for x in Interview.objects.all() if
                  x.user == User.objects.get(username=request.session['username'])]
    args['interviews'] = interviews
    if request.POST:
        dels = [x for x in request.POST if x.startswith("del")]
        viss = [x for x in request.POST if x.startswith("vis")]
        for x in dels:
            x = x.replace("del", "")
            interview = Interview.objects.get(pk=int(x))
            interview.delete()
        for x in viss:
            x = x.replace("vis", "")
            interview = Interview.objects.get(pk=int(x))
            interview.visible = True
            interview.save()
        for x in Interview.objects.all():
            if "vis" + str(x.id) not in viss and x.user == User.objects.get(username=request.session['username']):
                x.visible = False
                x.save()
        return redirect("/myinterviews", args)
    return render(request, "studtests/interviews.html", args)


def interview_result(request, int_id):
    args = {'username': request.session['username'], 'usertype': request.session['usertype']}
    interview = Interview.objects.get(pk=int_id)
    choices = [x for x in InterviewChoice.objects.all() if x.interview.id == interview.id]
    args['interview'], args['choices'] = interview, choices
    reslen = len([x for x in InterviewResult.objects.all() if x.choice.interview.id == interview.id])
    args['reslen'] = reslen
    return render(request, "studtests/interview_res.html", args)


@csrf_exempt
def send_avinterviews(request):
    user = User.objects.get(pk=int(request.POST.get('user')))
    interviews = request.POST.get("ints").split("/")
    checked = []
    availables = []
    stravailables = ""

    for x in InterviewResult.objects.all():
        if str(x.choice.interview.id) in interviews and x.user.id == user.id:
            checked.append(str(x.choice.interview.id))
    for x in interviews:
        if x not in str(checked):
            availables.append(x)
            stravailables += x + "/"
    stravailables = stravailables[:len(stravailables) - 1]
    print "checked" + str(checked)
    return HttpResponse(stravailables)


@csrf_exempt
def send_choices_id(request):
    ret = ""
    interview = Interview.objects.get(pk=int(request.POST.get("id")))
    choices = [x for x in InterviewChoice.objects.all() if x.interview.id == interview.id]
    for x in choices:
        ret += str(x.id) + "/"
    ret = ret[:len(ret) - 1]
    return HttpResponse(ret)


@csrf_exempt
def get_res(request):
    checked = False
    choice = InterviewChoice.objects.get(pk=int(request.POST.get("id")))
    choice.pick = str(int(choice.pick) + 1)
    choice.save()
    user = User.objects.get(pk=int(request.POST.get("user")))
    try:
        result = InterviewResult.objects.get(choice=choice, user=user)
        checked = True
    except:
        checked = False
    if not checked:
        result = InterviewResult(choice=choice, user=user)
        result.save()
    return HttpResponse("done")


@csrf_exempt
def send_choices_name(request):
    res = ""
    ids = request.POST.get("ids").split("/")
    for x in ids:
        choice = InterviewChoice.objects.get(pk=int(x))
        res += choice.name + "/"
    res = res[:len(res) - 1]
    return HttpResponse(res)


@csrf_exempt
def get_user(request):
    id = "None"
    print "login"
    try:
        user = auth.authenticate(username=request.POST.get('login'), password=request.POST.get('password'))
        auth.login(request, user)
        user_ = User.objects.get(username=request.POST.get("login"))
        print "login..."
        id = str(user_.id)
    except:
        pass
    return HttpResponse(id)


@csrf_exempt
def create_int_andr(request):
    int_name = request.POST.get("int_name")
    group = request.POST.get("group")
    choices = request.POST.get("choices").split("/")
    user = User.objects.get(pk=int(request.POST.get("user_id")))
    interview = Interview(name=int_name, user=user, group=group)
    exist = False
    try:
        int_ = Interview.objects.get(name=int_name)
        if int_.group == group:
            exist = True
    except:
        exist = False
    if not exist:
        interview.save()
        for x in choices:
            choice = InterviewChoice(interview=interview, name=x)
            choice.save()
            print choice
    return HttpResponse("done")


@csrf_exempt
def send_checked_ids(request):
    result = ""
    user = User.objects.get(pk=int(request.POST.get("user")))
    results = [x for x in InterviewResult.objects.all() if x.user.id == user.id]
    for x in results:
        result += str(x.choice.interview.id) + "/"
    return HttpResponse(result[:len(result) - 1])


@csrf_exempt
def lookresint(request):
    interview = Interview.objects.get(pk=int(request.POST.get("interview")))
    choices = [x for x in InterviewChoice.objects.all() if x.interview.id == interview.id]
    choicesstr = ""
    for x in choices:
        choicesstr += str(x) + "/" + str(x.pick) + "/"
    choicesstr = choicesstr[:len(choicesstr) - 1]
    return HttpResponse(choicesstr)