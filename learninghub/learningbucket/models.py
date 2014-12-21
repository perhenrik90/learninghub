from django.db import models
from django.contrib.auth.models import User
"""
Models for learning bucket
Here is where the e-learning projects are stored

@author Per-Henrik Kvalnes
"""

# E-learning project
class EProject(models.Model):

    name = models.CharField(max_length=40)
    timecreated = models.DateTimeField(auto_now_add=True)
    timeupdated = models.DateTimeField(auto_now=True)

    visits = models.IntegerField(default=0)
    organization = models.CharField(max_length=40)
    description = models.CharField(max_length=300)
    owner = models.ForeignKey(User)

#
# Describes a participant (person)
#
class EProjectParticipant(models.Model):

    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    organization = models.CharField(max_length=40)

#
# Links participant to project
#
class EProjectParticipantEntry(models.Model):
    role = models.CharField(max_length=50)
    write = models.BooleanField(default=False)

#
# One file to one instance of an EProject
#
class EProjectFile(models.Model):
    
    name = models.CharField(max_length=40,default="-")
    timecreated = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    filetype = models.CharField(max_length=20,
                                default="other")

    filepointer = models.FileField(upload_to='eprojects/%Y/%m/%d')
    
    owner_project = models.ForeignKey(EProject)


#
# EProject comment
#  
class EProjectComment(models.Model):
    
    comment = models.CharField(max_length=200)
    timecreated = models.DateTimeField(auto_now_add=True)
    project_owner = models.ForeignKey(EProject)
    owner = models.ForeignKey(User)
    

class EProjectTag(models.Model):
    
    tag = models.CharField(max_length=25)
    project = models.ForeignKey(EProject)

