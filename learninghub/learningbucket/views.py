from django.shortcuts import render
from django.template.response import TemplateResponse
from django.template import RequestContext, loader, Template
from django.http import HttpResponse

def login(request):
    template = loader.get_template('login.html')
    #template = Template("Hello World")
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
    

    
