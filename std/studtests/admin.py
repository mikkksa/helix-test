from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from studtests.models import Question, Choice, Subject, School, Student, Teacher, Test, TestResult, Grade, TimeTest, \
    ImQuestion, Interview, InterviewChoice, InterviewResult, News
import scorm_api.models as scmodels


class SubjectAdmin(admin.ModelAdmin):
    fields = ['subject', 'school']


class LawyerAdmin(admin.ModelAdmin):
    list_display = ('definition', 'image')

    def show_firm_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.firm_url)

    show_firm_url.short_description = "Firm URL"
    show_firm_url.allow_tags = True


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'edit_date'], 'classes': ['collapse']}),
        ('Subject', {'fields': ['subject']}),
        ('School', {'fields': ['school']}),
        ('Grade', {'fields': ['grade']}),
        ('Theme', {'fields': ['theme']}),
        ('Teacher', {'fields': ['teacher']}),
        ('Visible', {'fields': ['visibility']}),
        ('Test', {'fields': ['test']}),
        ('Enter', {'fields': ['enter']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'teacher', 'school', 'pub_date', 'edit_date')


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'student'


class UserAdmin(UserAdmin):
    inlines = (StudentInline,)


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
admin.site.register(Interview)
admin.site.register(InterviewChoice)
admin.site.register(InterviewResult)
admin.site.register(News, LawyerAdmin)
admin.site.register(scmodels.UploadedTinCan)
