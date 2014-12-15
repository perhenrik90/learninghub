import os
from django.shortcuts import render

from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.template import RequestContext, loader, Template, Context
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict

#
# Views for profilebucket
# All profile related views goes here
#
# @author Per-Henrik Kvalnes 2014
#


def profile(request):
    return "Test"
