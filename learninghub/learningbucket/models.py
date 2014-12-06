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
    owner = models.ForeignKey(User)
    visits = models.BigIntegerField()

