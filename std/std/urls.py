from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.resources import MyModelResource, TestModelResource, UserResource, StModelResource, SchoolResource, \
    GradeResource, QuestionResource, ChoiceResource, TestResultResource, ImquestionsResource
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(MyModelResource())
v1_api.register(TestModelResource())
v1_api.register(UserResource())
v1_api.register(StModelResource())
v1_api.register(SchoolResource())
v1_api.register(GradeResource())
v1_api.register(QuestionResource())
v1_api.register(ChoiceResource())
v1_api.register(TestResultResource())
v1_api.register(ImquestionsResource())

urlpatterns = patterns('',

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^studtests/', include('studtests.urls', namespace="studtests")),
                       url(r'^auth/', include('loginsys.urls')),
                       url(r'^api/', include(v1_api.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^', include('studtests.urls', namespace="studtests")),
                       )
