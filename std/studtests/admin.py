from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from studtests.models import Question, Choice, Subject, School,Student, Teacher, Test, TestResult, Grade, TimeTest, ImQuestion

class SubjectAdmin(admin.ModelAdmin):
    fields = ['subject', 'school']

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'edit_date'], 'classes': ['collapse']}),
        ('Subject', {'fields': ['subject']}),
        ('School', {'fields': ['school']}),
        ('Grade', {'fields': ['grade']}),
        ('Theme', {'fields': ['theme']}),
        ('Teacher', {'fields': ['teacher']}),
        ('Visible', {'fields': ['visibility']}),
        ('Test', {'fields': ['test']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'teacher', 'school', 'pub_date', 'edit_date')

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'student'

class UserAdmin(UserAdmin):
    inlines = (StudentInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Teacher)
admin.site.register(Choice)
admin.site.register(School)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Student)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(Grade)
admin.site.register(TimeTest)
admin.site.register(ImQuestion)