from django.conf.urls import patterns, include, url
from django.conf.urls.static import static


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # learning bucket app/module
    url(r'^$', 'learningbucket.views.login_view',name='Login'),
    url(r'^login/$', 'learningbucket.views.login_view', name='Login'),
    url(r'^logout/$', 'learningbucket.views.logout_view', name='Logout'),
    url(r'^error/$', 'learningbucket.views.error_view', name='Error'),

    url(r'^myprojects/$', 'learningbucket.views.myprojects', name='My Projects'),
    url(r'^createproject/$', 'learningbucket.views.createproject', name='Create project'),
    url(r'^project/$', 'learningbucket.views.project', name='Project'),
    url(r'^project/upload$', 
        'learningbucket.views.project_upload_file', 
        name='Upload'),
    url(r'^project/deletefile$', 
        'learningbucket.views.deleteFile', 
        name='Upload'),
    url(r'^project/edit$', 
        'learningbucket.views.editproject', 
        name='Edit'),
    url(r'^project/download$', 
        'learningbucket.views.project_download_file', 
        name='Upload'),
    url(r'^project/postcomment$', 
        'learningbucket.views.project_post_comment', 
        name='Upload'),

    # search bucket app/module 
    url(r'^search$','searchbucket.views.searchProjects',
        name='Search'),

    # profile bucket app/module
    url(r'^profile$','profilebucket.views.profile',
        name='Profile'),
    url(r'^profilemenu$','profilebucket.views.profile_menu',
        name='Profile Menu'),
    
    # admin app/module
    url(r'^admin/', include(admin.site.urls)),
)
