import os

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
import learninghub.settings as settings

import learningbucket.buckettools as buckettool



def userNotAuthenticated(request):
    return redirect("/login");

#
# Login view
#

def login_view(request):
    user = request.user
    c = {}
    if user.is_authenticated():
        return myprojects(request)

    if request.method == "POST":
        us = request.POST["username"] 
        pa = request.POST["pass"]         

        usr = authenticate(username=us, password=pa)
        if(usr is not None):
            login(request, usr)
            return redirect("/myprojects")
            
        # mark that the user has tried to login
        c["not_authenticated"] = 1
        
    template = loader.get_template('login.html')
    context = RequestContext(request, c)
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

    # get user related projects by updated date
    projects = models.EProject.objects.all().filter(owner=user).order_by('-timeupdated')
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
    is_owner = False

    # get for project id
    if(request.method == "GET" and 'id' in request.GET):
        get_id = request.GET["id"];
        eproject = models.EProject.objects.get(id=get_id)
        if eproject:
            template = loader.get_template("project.html")
            # if the user is the owner; set can_edit to true
    
        if(user.id == eproject.owner.id):
            is_owner = True

        if(is_owner == False):
            eproject.visits += 1
            eproject.save()
       
        # get files
        files = models.EProjectFile.objects.all().filter(owner_project=eproject)
        if files == None: files = []

        # get comments 
        comments = models.EProjectComment.objects.all().filter(project_owner=eproject)
        # prepare context
        c = {"project":eproject,"files":files, "is_owner":is_owner,
             "comments":comments}

    # render the template
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))


def deleteFile(request):

    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)    


    # get the project
    pid = request.GET['id']
    efile = models.EProjectFile.objects.get(id=pid)
    # if method is not post, show the editable things
    
    if efile.owner_project.owner.id != user.id:
        return error_view(request, _("You don't have the premission to delete this file!"))
    
    efile.filepointer.delete()
    efile.delete()
    
    newurl = '/project?id='+str(efile.owner_project.id)
    return redirect(newurl)
        
        



##########################
# Project post comment
###########################

def project_post_comment(request):
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)    

    elif request.method == "GET":
        return error_view(request, _("The comment has not been posted!"))

    # get post statements
    try:
        project_id = request.POST["id"]
        user = request.user
        comment = request.POST["comment"]
        p = models.EProject.objects.get(id=project_id)
        # create comment
        comment_model = models.EProjectComment(comment=comment, project_owner=p, owner=user)
        comment_model.save()
        
        # create and save tags
        taglist = buckettool.filterTags(comment)
        buckettool.storeTags(taglist=taglist, project=p)

        return redirect("/project?id="+project_id)

    except Exception as e:
        print(e)
        return error_view(request, _("The comment has not been posted!"))




##########################
# File handling views
##########################

# upload file
def project_upload_file(request):
    # no user, no file!
    user = request.user
    pid = 0
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)


    # handle post 
    if(request.method == "POST"):

        if not 'projectFile' in request.FILES:
            return error_view(request, _("No file was given."))

        # get post parameters
        pid = request.POST["project_id"]
        filetype = request.POST["filetype"]
        name = request.POST["name"]
        filep = request.FILES["projectFile"]

        project = models.EProject.objects.get(id=pid)

        pfile = models.EProjectFile(name=name,
                                    filetype=filetype,
                                    filepointer=filep,
                                    owner_project=project)
        pfile.save()
        project.save() # update time for project

        template = loader.get_template("project_uploadsuccess.html")
        c = {"file":pfile, "project":project}
        context = RequestContext(request, c)
        return HttpResponse(template.render(context))




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

# Download file
def project_download_file(request):

    user = request.user
    file_model = None

    if(not user.is_authenticated()):
        return userNotAuthenticated(request)    

    if('file_id' not in request.GET): 
        return error_view(request, _("No file were given!"))

    id = request.GET['file_id']
    file_model = models.EProjectFile.objects.get(id=id)
     

    file_model.filepointer.open("r")
    data = file_model.filepointer.read()
    file_model.filepointer.close();
    
    mimetype = 'application/force-download'
    response = HttpResponse(data, mimetype=mimetype)
    filename = os.path.basename(file_model.filepointer.url)
    response['Content-Disposition'] = "attachment; filename=%s" % (filename)

    
    return response




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



#
# Edit the project
#

def editproject(request):
    user = request.user
    if(not user.is_authenticated()): 
        return userNotAuthenticated(request)

    if('id' not in request.GET):
        return error_view(request,_("Can not edit a non existing project"))

    # get the project
    pid = request.GET['id']
    eproject = models.EProject.objects.get(id=pid)
    # if method is not post, show the editable things

    if eproject.owner.id != user.id:
        return error_view(request, _("You don't have the premission to edit this project!"))

    c = {} # c is the context

    # if method is post
    if(request.method == "POST"):
            pid = request.GET['id']
            eproject.name = request.POST['name']
            eproject.organizatoin = request.POST['organization']
            eproject.description = request.POST['description']
            c["updated"] = True
            eproject.save()


    
    c['project'] = eproject
    template = loader.get_template("editproject.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))

