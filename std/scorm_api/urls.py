from  django.conf.urls import patterns, url
from std import settings
from scorm_api import views

urlpatterns = patterns('',
                       url(r'^', views.index, name='scormind'),
                       )
