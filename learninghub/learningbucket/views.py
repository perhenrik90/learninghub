from django.shortcuts import render
from django.template.response import TemplateResponse
from django.template import RequestContext, loader, Template
from django.http import HttpResponse
from django.utils.translation import ugettext as _



def userNotAuthenticated(request):
    return login(request)

#
# Login view
#

def login(request):
    user = request.user

    template = loader.get_template('login.html')
    #template = Template("Hello World")
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
    

def myprojects(request):

    # if user is not authenticated!
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)
    
    template = loader.get_template("myprojects.html")
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))



def createproject(request):

    # if user is not authenticated!
    user = request.user
    if(not user.is_authenticated()):
        return userNotAuthenticated(request)

    template = loader.get_template("createproject.html")
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
