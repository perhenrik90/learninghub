from django.db import models
"""
Models for learning bucket
@author Per-Henrik Kvalnes
"""


class EProject(models.Model):
    # E-learning project
    name = models.CharField(max_length=40)
    

