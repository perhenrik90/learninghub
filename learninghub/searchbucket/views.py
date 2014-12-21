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

        # project dic
        pdic = {}

        # match list
        titles = [] #match on titles 
        tags = []   # match on tags
        users = []  # match on users
        
        # split the saerch tekst in to search terms
        terms = searchString.split(" ")

        # prioritize excat mathces in title
        titles += models.EProject.objects.filter(name__iregex=r'^.*'+searchString+'.*$')

        for term in terms:
            ## do multiple querys for every term and append to result list

            ## loop trough title results
            titles += models.EProject.objects.filter(name__iregex=r'^.*'+term+'.*$')
            for project in titles:
                if not hasattr(project, 'priority'):
                    project.priority = 1
                else: 
                    project.priority += 1

                if(project.id not in pdic):
                    pdic[project.id] = project
                else:
                    pdic[project.id].priority += project.priority
                
            tags += models.EProjectTag.objects.filter(tag=term).order_by('tag')
            tags += models.EProjectTag.objects.filter(tag='#'+term).order_by('tag')
            for tag in tags:
                project = tag.project
                if not hasattr(project, 'priority'):
                    project.priority = 1
                else: 
                    project.priority += 1

                if(project.id not in pdic):
                    pdic[project.id] = project
                else:
                    pdic[project.id].priority += project.priority
                


            users += User.objects.filter(first_name__iexact=term)
            users += User.objects.filter(last_name__iexact=term)

        # make the dictionary to a list and sort by priority
        s = lambda(x): x.priority
        pdic = sorted(pdic.values(),key=s, reverse=True)

        if len(users)> 0:
            c["users"] = users

        if len(pdic)> 0:
            c['projects'] = pdic

        c['results'] = True

    template = loader.get_template("search_project.html")
    context = RequestContext(request, c) 
    return HttpResponse(template.render(context))
