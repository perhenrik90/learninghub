from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib.auth import authenticate, login, logout
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


def logout_view(request):
    user = request.user
    if user.is_authenticated():
        logout(request)
        template = loader.get_template('logout.html')
        context = RequestContext(request, {'name':user.first_name})
        return HttpResponse(template.render(context))

    return redirect("/login")



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

###############################
# PROJECT VIEWS
###############################
# Lists projects for a user
#   

def myprojects(request):

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


def project(request):

    # if user is not authenticated!
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)

    # prepare to show the user that project do not exists
    template = loader.get_template("project_not_found.html")
    c = {}

    # get for project id
    if(request.method == "GET" and 'id' in request.GET):
        get_id = request.GET["id"];
        eproject = models.EProject.objects.get(id=get_id)
        if eproject:
            template = loader.get_template("project.html")


        # get files
        files = models.EProjectFile.objects.all().filter(owner_project=eproject)


        c = {"project":eproject,"files":files}        
    # render the template
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))

# File upload
def project_upload_file(request):
    # no user, no file!
    user = request.user
    pid = 0
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)

    # handle post 
    if(request.method == "POST"):
        pid = request.POST["project_id"]
        filetype = request.POST["filetype"]
        filep = request.FILES["projectFile"]

        print(filep)
        project = models.EProject.objects.get(id=pid)

        pfile = models.EProjectFile(filetype=filetype,
                                    filepointer=filep,
                                    owner_project=project)
        pfile.save()

        return error_view(request, _("Upload succses!."))



    # if no project id is given, display error.
    if 'id' not in request.GET:
        return error_view(request, _("No project is choosen."))

    if(request.method == "GET"):
        # on GET method 
        pid = request.GET["id"]
        template = loader.get_template("project_uploadfile.html")
        c = {"project_id":pid}
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
        desc  = request.POST["description"]

        eproject = models.EProject(name=pname,
                                   owner=user,
                                   organization=org,
                                   visits=0,
                                   description=desc)

        eproject.save()

        template = loader.get_template("createdproject.html")
        context = Context({"pname":pname})
        context.update(csrf(request))
        return HttpResponse(template.render(context))


    # normaly show a form 
    template = loader.get_template("createproject.html")
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
