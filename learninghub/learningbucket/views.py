import os

from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.utils import translation
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict

import learningbucket.models as models
import learninghub.settings as settings

import learningbucket.buckettools as buckettool

#
# Defines the views for the learning bucket
# This is the main views for the system
#
# @author Per-Henrik Kvalnes 2014
#


#
# what to do then a user is not loged in to the system
#
def userNotAuthenticated(request):
    return redirect(login_view);

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
            return redirect(myprojects)
            
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

    return redirect(login_view)



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

    if 'search' in request.GET:
        rx = r'.*'+request.GET["search"]+'.*'
        projects = models.EProject.objects.filter(owner=user,name__iregex=rx).order_by('-timeupdated')
        c = {"projects":projects, "search":request.GET["search"]}

        if len(projects) > 8:
            c["bigdata"] = True

    else:
        # get all user related projects by updated date
        projects = models.EProject.objects.all().filter(owner=user).order_by('-timeupdated')
        c = {"projects":projects}

        if len(projects) > 8:
            c["bigdata"] = True
    
    template = loader.get_template("myprojects.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))


#
# Display a project
#
def project(request):

    # if user is not authenticated!
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)


    # prepare to show the user that project do not exists
    template = loader.get_template("project_not_found.html")
    c = {}
    eproject = None
    is_owner = False

    # get for project id
    if(request.method == "GET" and 'id' in request.GET):
        get_id = request.GET["id"];
        eproject = models.EProject.objects.get(id=get_id)
        c = {}
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

        # check if user is following the project
        follow = models.EProjectFollower.objects.filter(user=request.user, project=eproject)
        if(len(follow) > 0):
            c['following'] = follow

    # render the template
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))


#
# Delete a project
#
def project_delete(request):

    # if user is not authenticated!
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)
    
    if(not 'project' in request.GET):
        return error_view(request, _("Can not delete a non exsisting project"))

    # get the project
    project = models.EProject.objects.get(id=request.GET['project'])
    c = {'project':project}

    # abort if the projects is not owned by the user
    if request.user != project.owner:
        return error_view(request, _("Can not delete another users project!"))

    # get the files
    project_files = models.EProjectFile.objects.filter(owner_project=project)
    if(len(project_files)>0):
        c['project_files'] = project_files

    # If the method is POST, the user need to authenticate
    if(request.method == "POST"):
        pwd = request.POST["password"]
        right_password = request.user.check_password(pwd)
        if(right_password):
            # delete files and the project
            for pfile in project_files: 
                pfile.filepointer.delete()
                pfile.delete()
            project.delete()

            c["project_deleted"] = True

        else:
            c["project_delete_fail"] = True


    template = loader.get_template('project_delete.html')
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))

##################################################
# Follow / unfollow a project
# The view acts like a toggle and does not have 
# its own template
##################################################
def project_follow(request):
    # if user is not authenticated!
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)


    # if no project given, send the user to errorview
    if('id' not in request.GET):
        return error_view(request, _("Not project given to follow."))

    p_id = request.GET["id"]
    projectmodel = models.EProject.objects.get(id=p_id)

    follower = models.EProjectFollower.objects.filter(user=request.user, project=projectmodel)
    if(len(follower) > 0):
        follower = follower[0]
        follower.delete()

    else:
        follower = models.EProjectFollower(user=request.user, project=projectmodel)
        follower.save()

    return redirect(reverse(project)+'?id='+p_id)

#
# Show projects the user are following
#
def projects_following(request):
    # if user is not authenticated!
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)    
    c = {}
    following = models.EProjectFollower.objects.filter(user=request.user)
    if(len(following)>0):
        c["following"] = following

    template = loader.get_template('projects_following.html')
    context = RequestContext(request,c)
    return HttpResponse(template.render(context))

#
# File views
#
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
    
    idstr = str(efile.owner_project.id)
    return redirect(reverse(project)+'?id='+idstr)
        
        



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

        return redirect(reverse(myprojects)+"?id="+project_id)

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

        # if the name is an empty string, give error message
        if len(name.strip()) <= 0:
            return error_view(request, _("A file must have a name. Can not upload a file with no name."))

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


#
# Add / remove participants 
# 

def project_participants(request):
    user = request.user
    if(not user.is_authenticated()): 
        return userNotAuthenticated(request)
    
    if 'project' not in request.GET:
        st = _("Can not add a participant to a non existing project.")
        return error_view(request, st)        

    project = models.EProject.objects.get(id=request.GET["project"])
    c = {"project_id":request.GET["project"], 'project':project}

    # get the project participants 
    participants = models.EProjectParticipant.objects.filter(project=project)
    if(participants > 0):
        c["participants"] = participants

    # do a search if there are a search string (ss)
    if 'searchstring' in request.GET:
        ss = request.GET["searchstring"]

        # search for every matching substring
        regex = r'^.*'+ss+'.*$'

        # search for both first and last name
        usrs = User.objects.filter(first_name__iregex=regex)
        usrs = usrs | User.objects.filter(last_name__iregex=regex)
        c["usermatches"] = usrs

    # if it is a post request, do add or delete
    if request.method == "POST":
        #
        # Add new participants 
        #
        if request.POST["operation"] == 'add':
            user_ids = request.POST["userid"]

            for u_id in user_ids:
                user = User.objects.get(id=u_id)
                participant = models.EProjectParticipant(usr=user, project=project)
                participant.save()

        #
        # Delete participants
        #
        elif request.POST["operation"] == "delete":
            participants_ids = request.POST["participantid"]
            for p_id in participants_ids:
                participant = models.EProjectParticipant.objects.get(id=p_id)
                participant.delete()

    template = loader.get_template("project_participants.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))    


#
# Dislpay the lated updates on project participating,
#  or following. 
#
def project_traffic(request):
    user = request.user
    if(not user.is_authenticated()): 
        return userNotAuthenticated(request)    
        
    c = {}
    user = request.user
    EProject = models.EProject
    participants = models.EProjectParticipant.objects.filter(usr=user).order_by('-project__timeupdated')[:10]
    c["participants"] = participants

    following = models.EProjectFollower.objects.filter(user=user).order_by('-project__timeupdated')[:10]
    c["following"] = following 

    template = loader.get_template("project_traffic.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))
