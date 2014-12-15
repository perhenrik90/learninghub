import os
from django.shortcuts import render

from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib.auth import authenticate, login, logout 
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

#
# Views for profilebucket
# All profile related views goes here
#
# @author Per-Henrik Kvalnes 2014
#


# called when user is not logged in 
def userNotAuthenticated(request):
    return redirect("/login");



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

    


    c["user"] = viewuser
    template = loader.get_template("profile.html");
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))
