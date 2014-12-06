from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^login/', 'learninghub.views.login', name='Login')
    # Examples:
    url(r'^login/$', 'learningbucket.views.login', name='Login'),
    url(r'^myprojects/$', 'learningbucket.views.myprojects', name='My Projects'),


    url(r'^admin/', include(admin.site.urls)),
)
