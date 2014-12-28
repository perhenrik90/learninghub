import os
from django.shortcuts import render

from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

from learningbucket.views import login_view
from profilebucket.models import UserProfile
from learningbucket.models import EProject
#
# Views for profilebucket
# All profile related views goes here
#
# @author Per-Henrik Kvalnes 2014
#


# called when user is not logged in 
def userNotAuthenticated(request):
    return redirect(login_view);



#
# Display an error to the user
#
def error_view(request, message=_("Unknown error")):
    user = request.user
    if user.is_authenticated():
        template = loader.get_template('private_error.html')
        context = RequestContext(request, {'message':message})
        return HttpResponse(template.render(context))
 
    return "Not yet implemented."


#
# Display menu for the profile 
#
def profile_menu(request):
    # if user is not authenticated!
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)

    c = {}    
    
    template = loader.get_template("profile_menu.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))



#
# Display a generic profile
# 

def profile(request):

    # if user is not authenticated!
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)

    c = {}

    if 'id' not in request.GET:
        return error_view(request, _("Can not show profile with an empty id"))

    uid = request.GET["id"]
    
    viewuser = User.objects.get(id=uid)

    if not viewuser:
        return error_view(request, _("This is not a valid user profile"))

    if(viewuser == request.user):
        c["is_owner"] = True

    user_profile = UserProfile.objects.all().filter(user_ref=viewuser)
    if(len(user_profile)>0): user_profile = user_profile[0]

    else: 
        user_profile = UserProfile(user_ref=viewuser)
        user_profile.save()

    c["user_auth"] = viewuser
    c["user_profile"] = user_profile

    template = loader.get_template("profile.html");
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))    


#
# Edit a user additional profile
#
def profile_update(request):
    # if user is not authenticated!
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)

    # update user information if it is a post request
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        bio = request.POST["bio"]
        email = request.POST["email"]

        user_profile = UserProfile.objects.all().filter(user_ref=user)

        if(len(user_profile) > 0):
            user_profile = user_profile[0]

        user_profile.bio = bio            
        user_profile.save()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        # go back to user profile
        return redirect(reverse(profile)+"?id="+str(user.id))

    # get user information 
    user_profile = UserProfile.objects.all().filter(user_ref=user)
    if(len(user_profile)<1):
        up = UserProfile(user_ref=user,bio="Wee")
        up.save()

    else:
        user_profile = user_profile[0]

    c = {"user_profile":user_profile}
    template = loader.get_template("profile_update.html");
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))        


def project_uploadimage(request):

    # no user, no file!
    user = request.user
    pid = 0
    c = {}

    if(not user.is_authenticated()):
        return userNotAuthenticated(request)

    # handle post 
    if(request.method == "POST"):

        if not 'profileImg' in request.FILES:
            return error_view(request, _("No file was given."))

        # get the profile
        user_profile = UserProfile.objects.all().filter(user_ref=user)
        if(len(user_profile)>0):
            user_profile = user_profile[0]
        else: 
            user_profile = UserProfile()

        user_profile.image = request.FILES['profileImg']
        user_profile.save()
        

    template = loader.get_template("profile_upload_img.html");
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))        

#
# Change password for a user
#

def profile_change_password(request):
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)
    
    c = {}

    if request.method == "POST":
        
        pwd1 = request.POST["password1"]
        pwd2 = request.POST["password2"]
        
        # if the passwords is not equal
        if pwd1 != pwd2:
            c = {"password_failed":True}

        # if the passwords are equal 
        elif pwd1 == pwd2:
            c = {"password_succes":True}
            request.user.set_password(pwd1)
            request.user.save()

    template = loader.get_template("profile_change_password.html");
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))        


#
# View projects owned by an user
#

def profile_projects(request):

    user = request.user
    c = {}

    if(not user.is_authenticated()):
        return userNotAuthenticated(request)

    if 'id' not in request.GET:
        return error_view(request, _("Can not show profile with an empty id"))

    uid = request.GET["id"]
    viewuser = User.objects.get(id=uid)

    if viewuser == request.user:
        c["is_owner"] = True

    # get projects
    projects = EProject.objects.all().filter(owner=viewuser)

    # load the profile image 
    user_profile = UserProfile.objects.all().filter(user_ref=viewuser)
    if(len(user_profile) > 0):
        user_profile = user_profile[0]

    c["user_auth"] = viewuser
    c["projects"] = projects
    c["user_profile"] = user_profile

    template = loader.get_template("profile_projects.html");
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))            
