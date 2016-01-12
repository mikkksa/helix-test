# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.tests.custom_user import CustomUser
from django.db import models
from multiprocessing.managers import public_methods
from django.db.models import Q, ImageField
from django.db.models.fields.related import ForeignKey
from django import forms
from django.template.defaultfilters import length, default
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.forms import UserCreationForm
import datetime
import os
import PIL


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class School(models.Model):
    school = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return self.school


class Grade(models.Model):
    grade = models.CharField(max_length=3)

    def __unicode__(self):
        return self.grade


class Subject(models.Model):
    subject = models.CharField(max_length=200)
    school = models.ForeignKey(School, null=True)

    def __unicode__(self):
        return self.subject


class Teacher(models.Model):
    user = models.OneToOneField(User, null=True)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    login = models.CharField(max_length=200)
    school = models.ForeignKey(School, null=True)

    def __unicode__(self):
        return self.name + ' ' + self.surname


class Test(models.Model):
    name = models.CharField(max_length=200, null=True)
    pub_date = models.DateTimeField('date published', default=datetime.datetime.now())
    edit_date = models.DateTimeField('date edited', default=datetime.datetime.now())
    choice_count = models.CharField(max_length=3, null=True)
    subject = models.ForeignKey(Subject, null=True)
    teacher = models.ForeignKey(Teacher, null=True)
    school = models.ForeignKey(School, null=True)
    grade = models.ForeignKey(Grade, null=True)
    theme = models.CharField(max_length=200, null=True)
    visibility = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class TimeTest(Test):
    time = models.CharField(max_length=3)

    def __unicode__(self):
        return self.name


class RndTest(Test):
    qcount = models.CharField(max_length=3)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=datetime.datetime.now())
    edit_date = models.DateTimeField('date edited', default=datetime.datetime.now())
    subject = models.ForeignKey(Subject, null=True)
    teacher = models.ForeignKey(Teacher, null=True)
    school = models.ForeignKey(School, null=True)
    grade = models.ForeignKey(Grade, null=True)
    theme = models.CharField(max_length=200)
    visibility = models.BooleanField(default=False)
    test = models.ForeignKey(Test, null=True)

    def __unicode__(self):
        return self.question_text


class ImQuestion(Question):
    image = models.ImageField()


class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, null=True)
    right_choice = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Question: ' + self.question.question_text + '         Answer:       ' + self.choice_text


class Student(models.Model):
    user = models.OneToOneField(User, null=True)
    name = models.CharField(max_length=200, null=True)
    surname = models.CharField(max_length=200, null=True)
    login = models.CharField(max_length=200, null=True)
    school = models.ForeignKey(School, null=True)
    grade = models.ForeignKey(Grade, null=True)
    question_list = models.ManyToManyField(Test, blank=True, null=True)

    def set_password(self, raw_password):
        self.user.set_password(raw_password)

    def __unicode__(self):
        return self.name + ' ' + self.surname


class TestResult(models.Model):
    student = models.ForeignKey(Student)
    test = models.ForeignKey(Test)
    balls = models.CharField(max_length=5)
    quest_count = models.CharField(max_length=5, null=True)
    right_choices = models.ManyToManyField(Choice, related_name="right")
    unright_choices = models.ManyToManyField(Choice, related_name="false")
    right_count = models.CharField(max_length=3, null=True)
    unright_count = models.CharField(max_length=3, null=True)
    answers_count = models.CharField(max_length=3, null=True)

    def __unicode__(self):
        return 'Student: ' + str(self.student) + '; Test: ' + str(self.test) + ';  Right: ' + str(
            len(self.right_choices.all())) \
               + '; Unright: ' + str(len(self.unright_choices.all())) + ' from' + ' ' + self.quest_count \
               + ' questions and ' + str(self.test.choice_count) + ' right choices' + ' from ' + str(
            4 * len(self.test.question_set.all())) \
               + ' choices'


class RegistrTeacherForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = ['name', 'surname', 'school']


class RegistrStudentForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'school', 'grade']


class UploadFileForm(forms.Form):
    file = forms.FileField()


class Interview(models.Model):
    user = models.ForeignKey(User, null=True)
    group = models.CharField(max_length=40, default="")
    name = models.CharField(max_length=80)
    visible = models.BooleanField(default=True)
    pub_date = models.DateTimeField('date published', default=datetime.datetime.now())
    edit_date = models.DateTimeField('date edited', default=datetime.datetime.now())

    def __unicode__(self):
        return self.name


class InterviewChoice(models.Model):
    interview = models.ForeignKey(Interview)
    name = models.CharField(max_length=60)
    pub_date = models.DateTimeField('date published', default=datetime.datetime.now())
    edit_date = models.DateTimeField('date edited', default=datetime.datetime.now())
    pick = models.CharField(max_length=5, default=0)

    def __unicode__(self):
        return self.name


class InterviewResult(models.Model):
    choice = models.ForeignKey(InterviewChoice)
    user = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.choice.name