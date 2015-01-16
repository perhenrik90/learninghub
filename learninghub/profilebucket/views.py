import os
import re
import sha
import datetime

from django.shortcuts import render
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.models import get_current_site
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

from learninghub import settings
from learningbucket.views import login_view
from profilebucket.models import UserProfile
from profilebucket.models import UserSkill
from profilebucket.models import PwdValidationCode
from profilebucket.models import UsrValidationCode
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

    # set is owner 
    if(viewuser == request.user):
        c["is_owner"] = True

    # get skills
    skills = UserSkill.objects.filter(user=viewuser)
    if(len(skills)>0):
        c["skills"] = skills
        
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

#
# Add a skill to a user
#
def profile_add_skill(request):
    # if user is not authenticated!
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)

    # if the method is not post 
    if not request.method == "POST" and not 'skill' in request.POST:
        error_view(request, _("No skill given"))

    c = {}
    skill = request.POST["skill"]
    usr = request.user
    
    s = UserSkill(skill=skill, user=usr)
    s.save()
    return redirect(reverse(profile)+'?id='+str(usr.id))

    template = loader.get_template("profile.html");
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))


#
# Upload an profile image 
#
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

##################################################################
#     PASSWORD VALIDATION 
##################################################################

#
# Request a new password by email
#
def profile_lostpwd(request):
    c = {}
    reglist = [r'.*@nlsh.no']

    # if email defined 
    if 'email' in request.POST and request.method == "POST":
        email = request.POST["email"]
        # check if the mail is valid
        if(re.match(r'\b[\w.-]+@[\w.-]+.\w{2,4}\b', email)):
            c = {'email':email}
            usrs = User.objects.filter(email=email)
            # if user is found
            if(len(usrs)>0):
                usr = usrs[0]
                # generate a validation code 
                time = datetime.datetime.now()
                code = time.year+time.day+time.minute
                code = sha.new(str(code)+email).hexdigest()
                print(code)
                m = PwdValidationCode(code=code, owner=usr)
                m.save()
                
                # generate email
                full_url = settings.SITE_URL+reverse(profile_validatePwdCode)+'?pwdcode='+code
                
                message = _("You have requested a new password: ")+ full_url
                print(message)
                send_mail(_("Password reset"),message, settings.HOST_EMAIL, [usr.email])
            
        else:
            c = {"not_valid_mail":True}

    template = loader.get_template("profile_lostpwd.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))


#
# Validate pwd code
#
def profile_validatePwdCode(request):
    c = {}

    if request.method == "POST":
        pwdcode = request.POST["pwdcode"]
        pwd1 = request.POST["pass1"]
        pwd2 = request.POST["pass2"]

        tokens = PwdValidationCode.objects.filter(code=pwdcode)
        if(len(tokens)>0):
            token = tokens[0]     

            if pwd1 == pwd2 and pwd1 != "":
                token.owner.set_password(pwd1)
                usr = User.objects.get(id=token.owner.id)
                usr.set_password(pwd1)
                usr.save()
                token.delete()
                c["success"] = True

            else:
                c["pwd_not_equal"] = True

        template = loader.get_template("profile_validatepwdcode.html")
        context = RequestContext(request, c)
        return HttpResponse(template.render(context))

    # if no password are given
    if 'pwdcode' in request.GET:
        pwdcode = request.GET["pwdcode"]
        c["pwdcode"] = pwdcode

        tokens = PwdValidationCode.objects.filter(code=pwdcode)
        if(len(tokens)>0):
            token = tokens[0]
        
        else:
            c["notvalid"] = True

    else:
        c["notvalid"] = True
        
        
    template = loader.get_template("profile_validatepwdcode.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))

###################################
# Create a new uesr (if allowed)
###################################

def profile_createusr(request):

    c = {}
    
    # if the user try to create 
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]        
        pwd1 = request.POST["pwd1"]
        pwd2 = request.POST["pwd2"]

        # check if ther is a real name
        if not first_name.strip() or not last_name.strip():
            c["not_valid"] = _("You must enter a valid name")

        if not re.match(r'\b[\w.-]+@[\w.-]+.\w{2,4}\b', email):
            c["not_valid"] = _("You must enter a valid email")

        # check if passwords are equal 
        if pwd1.strip() and pwd1 != pwd2:
            c["not_valid"] = _("The passwords are not equal")

        # if there are no errors, create a user
        if not 'not_valid' in c:
            usr = User(username=email,
                       first_name=first_name,
                       last_name=last_name,
                       email=email,
                       is_active=False)
            usr.set_password(pwd1)
            usr.save()
            code = UsrValidationCode(owner=usr)
            code.save()
            message = _("You have created a new user.\n")
            message += _("Confirm with the url following url.\n\n")
            message += settings.SITE_URL + reverse(profile_validateusr)+'?code='+code.code
            send_mail(_("Activate your user."), message, settings.HOST_EMAIL,[email])
            print(message)
            c["usr"] = usr
            c["success"] = True

    template = loader.get_template("profile_createusr.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))    

#
# Set an user to is_active based on a validation url 
#
def profile_validateusr(request):
    c = {}
    if 'code' in request.GET:
        c = {'success':True}
        try:
            code = UsrValidationCode.objects.get(code=request.GET["code"])
            code.owner.is_active = True
            code.owner.save()
            code.delete()
        except Exception:
            return error_view(request, _("This code is not valid"))

    template = loader.get_template("profile_validateusr.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))        
