from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.template import RequestContext, loader, Template, Context

# import models from learning bucket
import learningbucket.models as models


def searchProjects(request):
    
    c = {"results":False}

    if 'tags' in request.GET:
        searchString = request.GET['tags']
        searchString = searchString.lower()

        # tags = result list 
        tags = []

        # split the saerch tekst in to search terms
        terms = searchString.split(" ")

        for term in terms:
            ## do multiple querys for every term and append to result list
            tags += models.EProjectTag.objects.all().filter(tag=term).order_by('tag')
            tags += models.EProjectTag.objects.all().filter(tag='#'+term).order_by('tag')

        c['tags'] = tags
        c['results'] = True

    template = loader.get_template("search_project.html")
    context = RequestContext(request, c) 
    return HttpResponse(template.render(context))
