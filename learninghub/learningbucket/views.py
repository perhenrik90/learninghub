from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib.auth import authenticate, login
from django.forms.models import model_to_dict

import learningbucket.models as models

def userNotAuthenticated(request):
    return redirect("/login");

#
# Login view
#

def login_view(request):
    user = request.user
    if user.is_authenticated():
        return myprojects(request)

    if request.method == "POST":
        us = request.POST["username"] 
        pa = request.POST["pass"]         

        usr = authenticate(username=us, password=pa)
        if(user is not None):
            login(request, usr)
            return redirect("/myprojects")
        
        
    template = loader.get_template('login.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
 
#
# Lists projects for a user
#   

def myprojects(request):
    print(translation.get_language())
    # if user is not authenticated!
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)

    projects = models.EProject.objects.all().filter(owner=user)
    print(projects)
    c = {"projects":projects}
    
    template = loader.get_template("myprojects.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))


#
# Form for create a new project!
#

def createproject(request):

    # if user is not authenticated!
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)

    # on post, create a project!
    if(request.method == "POST"):
        # variable from the post to be used
        pname = request.POST["name"]
        org   = request.POST["organization"]

        eproject = models.EProject(name=pname,
                                   owner=user,
                                   organization=org,
                                   visits=0)

        eproject.save()

        template = loader.get_template("createdproject.html")
        context = Context({"pname":pname})
        context.update(csrf(request))
        return HttpResponse(template.render(context))


    # normaly show a form 
    template = loader.get_template("createproject.html")
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
