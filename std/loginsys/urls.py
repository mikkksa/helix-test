from  django.conf.urls import  patterns, url
from loginsys import  views

urlpatterns = patterns('',
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^registrate', views.registrate, name='registrate'),
    url(r'^action',views.user_choose, name='action')
)