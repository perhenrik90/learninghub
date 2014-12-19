from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.template import RequestContext, loader, Template, Context
from django.contrib.auth.models import User

# import models from learning bucket
import learningbucket.models as models

#
# Defines views for searching in projects
# @author Per-Henrik Kvalnes 2014
#

# search based on tag names
def searchProjects(request):
    
    c = {"results":False}

    if 'tags' in request.GET:
        searchString = request.GET['tags']
        searchString = searchString.lower()

        # tags = result list 
        tags = []
        users = []

        # split the saerch tekst in to search terms
        terms = searchString.split(" ")

        for term in terms:
            ## do multiple querys for every term and append to result list
            tags += models.EProjectTag.objects.all().filter(tag=term).order_by('tag')
            tags += models.EProjectTag.objects.all().filter(tag='#'+term).order_by('tag')
            users += User.objects.all().filter(first_name__iexact=term)
            users += User.objects.all().filter(last_name__iexact=term)
            
        print(users)
        c["users"] = users
        c['tags'] = tags
        c['results'] = True

    template = loader.get_template("search_project.html")
    context = RequestContext(request, c) 
    return HttpResponse(template.render(context))
