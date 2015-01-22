# -*- coding: utf-8 -*-
from django.db import models

#
# Models related to searching
#
# @author Per-Henrik Kvalnes 2014
#


# Count times a tag is searched for
class TagCounter(models.Model):
    
    tag = models.CharField(max_length=100)
    counter = models.IntegerField(default=0)

