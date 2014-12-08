from django.conf.urls import patterns, include, url
from django.conf.urls.static import static


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # learning bucket app/module
    url(r'^login/$', 'learningbucket.views.login_view', name='Login'),
    url(r'^logout/$', 'learningbucket.views.logout_view', name='Logout'),
    url(r'^error/$', 'learningbucket.views.error_view', name='Error'),

    url(r'^myprojects/$', 'learningbucket.views.myprojects', name='My Projects'),
    url(r'^createproject/$', 'learningbucket.views.createproject', name='Create project'),
    url(r'^project/$', 'learningbucket.views.project', name='Project'),
    url(r'^project/upload$', 
        'learningbucket.views.project_upload_file', 
        name='Upload'),
    url(r'^project/postcomment$', 
        'learningbucket.views.project_post_comment', 
        name='Upload'),
                    

    # admin app/module
    url(r'^admin/', include(admin.site.urls)),
)
