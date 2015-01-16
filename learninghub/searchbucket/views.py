from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.template import RequestContext, loader, Template, Context

from django.contrib.auth.models import User

# import models from learning bucket
from django.db.models import Count
from profilebucket.models import UserSkill

import learningbucket.models as models

#
# Defines views for searching in projects
# @author Per-Henrik Kvalnes 2014
#

#
# search based on tag names
#
def searchProjects(request):
    
    c = {"results":False}

    if 'tags' in request.GET:
        searchString = request.GET['tags']
        searchString = searchString.lower()

        # dictionaries is used to create a priority map
        # the keyvalue is the object unique id
        pdic = {} # map for projects
        udic = {} # map for users

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

            # loop trought tags
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
                

            # search on users
            users += User.objects.filter(first_name__iregex=r'^.*'+term+'.*$')
            users += User.objects.filter(last_name__iregex=r'^.*'+term+'.*$')

            for user in users:
                if not hasattr(user, 'priority'):
                    user.priority = 1
                else:
                    user.priority += 1
                    
                if user.id in udic:
                    udic[user.id].priority += user.priority
                else:
                    udic[user.id] = user
            
        # make the dictionary to a list and sort by priority
        #  on users and projects
        s = lambda(x): x.priority
        pdic = sorted(pdic.values(),key=s, reverse=True)
        users = sorted(udic.values(), key=s, reverse=True)

        if len(users)> 0:
            c["users"] = users

        if len(pdic)> 0:
            c['projects'] = pdic

        c['results'] = True

    template = loader.get_template("search_project.html")
    context = RequestContext(request, c) 
    return HttpResponse(template.render(context))

#
# Counts the top used tags
#  and presents them
#
def topTags(request):
    c = {}
    taglist = models.EProjectTag.objects.values('tag').annotate(dcount=Count('tag'))\
              .order_by('-dcount')[:20]

    if(len(taglist)>0):
        c["tags"] = taglist
 
    template = loader.get_template("toptags.html")
    context = RequestContext(request, c) 
    return HttpResponse(template.render(context))


#
# Gets all users with a spesific skill
#
def usersSkill(request):
    c = {}
    

    skill = "Utvikling"
    c["skill"] = skill
    skills = UserSkill.objects.filter(skill=skill)
    
    if(len(skills) > 0):
        c["skills"] = skills

    template = loader.get_template("usersskill.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))
