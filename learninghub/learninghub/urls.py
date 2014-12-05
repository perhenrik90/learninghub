from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^login/', 'learninghub.views.login', name='Login')
    # Examples:
    url(r'^login/$', 'learningbucket.views.login', name='Login'),
    #url(r'^login/', include('learningbucket.views.login')),

    url(r'^admin/', include(admin.site.urls)),
)
