from django.shortcuts import render
from django.template.response import TemplateResponse
from django.template import RequestContext, loader, Template
from django.http import HttpResponse
from django.utils.translation import ugettext as _

#
# Login view
#

def login(request):
    user = request.user
    if(user.is_authenticated()):
        print("User is logn in!")

    _("Login")
    template = loader.get_template('login.html')
    #template = Template("Hello World")
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
    

    
