from django.conf.urls import patterns, include, url
from django.conf.urls.static import static



from django.contrib import admin
import settings 

admin.autodiscover()

up = "" # prefix

urlpatterns = patterns('',
    # learning bucket app/module
    url(r'^'+up+'$', 'learningbucket.views.login_view',name='Login'),
    url(r'^'+up+'login/$', 'learningbucket.views.login_view', name='Login'),
    url(r'^'+up+'logout/$', 'learningbucket.views.logout_view', name='Logout'),
    url(r'^'+up+'error/$', 'learningbucket.views.error_view', name='Error'),

    url(r'^'+up+'myprojects/$', 'learningbucket.views.myprojects', name='My Projects'),
    url(r'^'+up+'createproject/$', 'learningbucket.views.createproject', name='Create project'),
    url(r'^'+up+'project/$', 'learningbucket.views.project', name='Project'),
    url(r'^'+up+'project/delete$', 'learningbucket.views.project_delete', name='Project Delete'),
    url(r'^'+up+'project/follow$', 'learningbucket.views.project_follow', name='Project Follow'),
    url(r'^'+up+'project/following$', 'learningbucket.views.projects_following', name='Projects Following'),
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
    url(r'^'+up+'project/participants$', 
        'learningbucket.views.project_participants', 
        name='Project Participants'),
    url(r'^'+up+'project/traffichall$', 
        'learningbucket.views.project_traffic', 
        name='Traffic Hall'),

    # search bucket app/module 
    url(r'^'+up+'search$','searchbucket.views.searchProjects',
        name='Search'),
    # search bucket app/module 
    url(r'^'+up+'search/toptags$','searchbucket.views.topTags',
        name='Top tags'),

    # profile bucket app/module
    url(r'^'+up+'profile$','profilebucket.views.profile',
        name='Profile'),
    url(r'^'+up+'profilemenu$','profilebucket.views.profile_menu',
        name='Profile Menu'),
    url(r'^'+up+'profilepassword$','profilebucket.views.profile_change_password',
        name='Profile Menu'),
    url(r'^'+up+'profileupdate$','profilebucket.views.profile_update',
        name='Profile Update'),
    url(r'^'+up+'profile/addskill$','profilebucket.views.profile_add_skill',
        name='Profile Update'),
    url(r'^'+up+'profileupload$','profilebucket.views.project_uploadimage',
        name='Profile Upload'),
    url(r'^'+up+'profileprojects$','profilebucket.views.profile_projects',
        name='Profile Projects'),
    url(r'^'+up+'lostpwd$','profilebucket.views.profile_lostpwd',
        name='Lost Password'),
    url(r'^'+up+'validatepwdcode$','profilebucket.views.profile_validatePwdCode',
        name='Validate Pwd Code'),
    url(r'^'+up+'createusr$','profilebucket.views.profile_createusr',
        name='Create User'),
    url(r'^'+up+'validateusr$','profilebucket.views.profile_validateusr',
        name='Validate User'),
    
    # admin app/module
    url(r'^'+up+'admin/', include(admin.site.urls)),


   
    # only make the profile images public (accessable through url) 
) +  static(settings.MEDIA_URL+"profileimg/", document_root=settings.MEDIA_ROOT+"profileimg/")
print settings.MEDIA_ROOT
