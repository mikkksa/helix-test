# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from studtests.models import RegistrTeacherForm, RegistrStudentForm, Subject, School, Student, Teacher, Grade
from django.contrib.auth.models import User
import studtests


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['username'] = username
            teachers = Teacher.objects.all()
            students = Student.objects.all()
            for teacher in teachers:
                if teacher.login == username:
                    request.session['usertype'] = "t"
                    request.session['questions'] = []
            for student in students:
                if student.login == username:
                    request.session['usertype'] = "s"
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('loginsys/login.html', args)
    else:
        return render_to_response('loginsys/login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/')


def registrate(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.session['usertype'] == "t":
        args['form1'] = RegistrTeacherForm()
    else:
        args['form1'] = RegistrStudentForm()
    if request.session['usertype'] is not None:
        if request.POST.get("reg"):
            newuser_form = UserCreationForm(request.POST)
            newteacher_form = RegistrTeacherForm(request.POST)
            newstudent_form = RegistrStudentForm(request.POST)
            if newuser_form.is_valid() and (newteacher_form.is_valid() or newstudent_form.is_valid):
                school = School.objects.get(id=request.POST['school'])
                newuser_form.save()
                new_user = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                             password=newuser_form.cleaned_data['password2'])
                request.session['username'] = newuser_form.cleaned_data['username']
                auth.login(request, new_user)
                if request.session['usertype'] == "t":
                    newteacher = Teacher(user=User.objects.get(username=newuser_form.cleaned_data['username']),
                                         school=school, name=request.POST['name'], login=request.POST['username'],
                                         surname=request.POST['surname'])
                    newteacher.save()
                elif request.session['usertype'] == "s":
                    newstudent = Student(grade=Grade.objects.get(id=request.POST['grade']),
                                         user=User.objects.get(username=newuser_form.cleaned_data['username']),
                                         school=school, name=request.POST['name'], login=request.POST['username'],
                                         surname=request.POST['surname'])
                    newstudent.save()

                return redirect('/')
            else:
                if request.session['usertype'] == "t":
                    args['form1'] = RegistrTeacherForm(request.POST)
                else:
                    args['form1'] = RegistrStudentForm(request.POST)
        return render_to_response('loginsys/registrate.html', args)


def user_choose(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        if request.POST.get("teacher"):
            request.session['usertype'] = "t"
        else:
            request.session['usertype'] = "s"
        return HttpResponseRedirect(reverse('registrate'))
    return render_to_response('loginsys/action.html', args)
