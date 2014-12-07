from django.conf.urls import patterns, include, url
from django.conf.urls.static import static


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^login/', 'learninghub.views.login', name='Login')
    # Examples:
    url(r'^login/$', 'learningbucket.views.login_view', name='Login'),
    url(r'^logout/$', 'learningbucket.views.logout_view', name='Logout'),
    url(r'^myprojects/$', 'learningbucket.views.myprojects', name='My Projects'),

    url(r'^createproject/$', 'learningbucket.views.createproject', name='Create project'),
    url(r'^project/$', 'learningbucket.views.project', name='Project'),

    url(r'^admin/', include(admin.site.urls)),
)
