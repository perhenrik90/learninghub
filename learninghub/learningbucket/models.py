from django.db import models
from django.contrib.auth.models import User
"""
Models for learning bucket
Here is there the e-learning projects are stored

@author Per-Henrik Kvalnes
"""

# E-learning project
class EProject(models.Model):

    name = models.CharField(max_length=40)
    timecreated = models.DateTimeField(auto_now_add=True)
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
    
    project = models.ForeignKey(EProject)
    participant = models.ForeignKey(EProjectParticipant)

    role = models.CharField(max_length=50)
    write = models.BooleanField(default=False)

class EProjectFile(models.Model):
    


    type = models.CharField(max_length=40)
    timecreated = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    filetype = models.CharField(max_length=20,
                                default="other")

    owner_project = models.ForeignKey(EProject)
    
