from django.conf.urls import patterns, include, url
from django.conf.urls.static import static


from django.contrib import admin
admin.autodiscover()

up = "lh/" # prefix

urlpatterns = patterns('',
    # learning bucket app/module
    url(r'^'+up+'$', 'learningbucket.views.login_view',name='Login'),
    url(r'^'+up+'login/$', 'learningbucket.views.login_view', name='Login'),
    url(r'^'+up+'logout/$', 'learningbucket.views.logout_view', name='Logout'),
    url(r'^'+up+'error/$', 'learningbucket.views.error_view', name='Error'),

    url(r'^'+up+'myprojects/$', 'learningbucket.views.myprojects', name='My Projects'),
    url(r'^'+up+'createproject/$', 'learningbucket.views.createproject', name='Create project'),
    url(r'^'+up+'project/$', 'learningbucket.views.project', name='Project'),
    url(r'^'+up+'project/upload$', 
        'learningbucket.views.project_upload_file', 
        name='Upload'),
    url(r'^'+up+'project/deletefile$', 
        'learningbucket.views.deleteFile', 
        name='Upload'),
    url(r'^'+up+'project/edit$', 
        'learningbucket.views.editproject', 
        name='Edit'),
    url(r'^'+up+'project/download$', 
        'learningbucket.views.project_download_file', 
        name='Upload'),
    url(r'^'+up+'project/postcomment$', 
        'learningbucket.views.project_post_comment', 
        name='Upload'),

    # search bucket app/module 
    url(r'^'+up+'search$','searchbucket.views.searchProjects',
        name='Search'),

    # profile bucket app/module
    url(r'^'+up+'profile$','profilebucket.views.profile',
        name='Profile'),
    url(r'^'+up+'profilemenu$','profilebucket.views.profile_menu',
        name='Profile Menu'),
    url(r'^'+up+'profilepassword$','profilebucket.views.profile_change_password',
        name='Profile Menu'),
    url(r'^'+up+'profileupdate$','profilebucket.views.profile_update',
        name='Profile Update'),
    
    # admin app/module
    url(r'^'+up+'admin/', include(admin.site.urls)),
)
