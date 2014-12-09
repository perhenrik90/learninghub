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
    
    c = {}
    template = loader.get_template("search_project.html")
    context = RequestContext(request, c)
    return HttpResponse(template.render(context))
