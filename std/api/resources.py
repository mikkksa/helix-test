# from django.contrib.auth.models import User
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from studtests.models import Teacher, Subject, Test, Student, School, Grade, Choice, Question, TestResult, ImQuestion, \
    Interview, InterviewResult, InterviewChoice, User
from tastypie.authentication import Authentication
from tastypie import fields
from tastypie.serializers import Serializer


class SchoolResource(ModelResource):
    class Meta:
        limit = 0
        queryset = School.objects.all()
        resource_name = 'schools'
        allowed_methods = ['get']
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])


class GradeResource(ModelResource):
    class Meta:
        limit = 0
        queryset = Grade.objects.all()
        resource_name = 'grades'
        allowed_methods = ['get']
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])


class UserResource(ModelResource):
    class Meta:
        limit = 0
        queryset = User.objects.all()
        resource_name = 'users'
        allowed_methods = ['get']
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])


class MyModelResource(ModelResource):
    def dehydrate(self, bundle):
        try:
            school = School.objects.filter(id=bundle.obj.school.id)
            user = User.objects.filter(id=bundle.obj.user.id)
            bundle.data['user'] = user[0].id
            bundle.data['school'] = school[0].id
        except School.DoesNotExist:
            pass
        except User.DoesNotExist:
            pass
        return bundle

    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True)
    school = fields.ForeignKey(SchoolResource, 'school', null=True, blank=True)

    class Meta:
        limit = 0
        queryset = Teacher.objects.all()
        resource_name = 'teachers'
        allowed_methods = ['get']
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])


class TestModelResource(ModelResource):
    def dehydrate(self, bundle):
        try:
            teacher = Teacher.objects.filter(id=bundle.obj.teacher.id)
            bundle.data['teacher'] = teacher[0].id
        except Teacher.DoesNotExist:
            pass
        return bundle

    teacher = fields.ForeignKey(MyModelResource, 'teacher', null=True)

    class Meta:
        limit = 0
        queryset = Test.objects.all()
        resource_name = 'tests'
        allowed_methods = ['get']
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])


class QuestionResource(ModelResource):
    def dehydrate(self, bundle):
        try:
            test = Test.objects.filter(id=bundle.obj.test.id)
            count = 0
            chcount = len([x for x in Choice.objects.all() if x.question_id == bundle.obj.id])
            for x in Question.objects.all():
                test2 = Test.objects.get(pk=test[0].id)
                if x.test == test2:
                    count += 1
            bundle.data['test'] = test[0].id
            bundle.data['choice_count'] = chcount
            bundle.data['question_count'] = count
        except Test.DoesNotExist:
            pass
        return bundle

    test1 = fields.ForeignKey(TestModelResource, 'test', null=True)

    class Meta:
        limit = 0
        queryset = Question.objects.all()
        resource_name = 'questions'
        allowed_methods = ['get']
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])


class ChoiceResource(ModelResource):
    def dehydrate(self, bundle):
        try:
            question = Question.objects.filter(id=bundle.obj.question.id)
            bundle.data['question'] = question[0].id
            bundle.data['test'] = question[0].test.id
        except Test.DoesNotExist:
            pass
        return bundle

    question = fields.ForeignKey(QuestionResource, 'question', null=True)

    class Meta:
        limit = 0
        queryset = Choice.objects.all()
        resource_name = 'choices'
        allowed_methods = ['get']
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])


class TestResultResource(ModelResource):
    def dehydrate(self, bundle):
        try:
            test = Test.objects.filter(id=bundle.obj.test.id)
            bundle.data['test'] = test[0].id
        except Test.DoesNotExist:
            pass
        return bundle

    class Meta:
        queryset = TestResult.objects.all()
        resource_name = 'testresults'
        allowed_methods = ['get']
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])


class StModelResource(ModelResource):
    def dehydrate(self, bundle):
        try:
            grade = Grade.objects.filter(id=bundle.obj.grade.id)
            school = School.objects.filter(id=bundle.obj.school.id)
            user = User.objects.filter(id=bundle.obj.user.id)
            bundle.data['user'] = user[0].id
            bundle.data['school'] = school[0].id
            bundle.data['grade'] = grade[0].id
        except Test.DoesNotExist:
            pass
        except Grade.DoesNotExist:
            pass
        return bundle

    user = fields.ForeignKey(UserResource, 'user', null=True)
    school = fields.ForeignKey(SchoolResource, 'school', null=True)
    grade = fields.ForeignKey(GradeResource, 'grade', null=True)

    class Meta:
        limit = 0
        queryset = Student.objects.all()
        resource_name = 'students'
        allowed_methods = ['get']
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])


class ImquestionsResource(ModelResource):
    class Meta:
        limit = 0
        queryset = ImQuestion.objects.all()
        resource_name = 'imquestions'
        allowed_methods = ['get']
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])


class InterviewResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True)

    def dehydrate(self, bundle):
        try:
            user = User.objects.filter(id=bundle.obj.user.id)
            bundle.data['user'] = user[0].id
        except:
            pass
        return bundle

    class Meta:
        limit = 0
        queryset = Interview.objects.all()
        resource_name = 'interviews'
        allowed_methods = ['get']
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])


class InterviewChoiceResource(ModelResource):
    interview = fields.ForeignKey(InterviewResource, 'interview', null=True)

    class Meta:
        limit = 0
        queryset = InterviewChoice.objects.all()
        resource_name = 'interview_choices'
        allowed_method = ['get']
        serializer = Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])
