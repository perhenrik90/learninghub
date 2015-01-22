# -*- coding: utf-8 -*-
import datetime
import sha

from django.db import models
from django.contrib.auth.models import User

#
# Describes models related to user profiles and user 
# statistics 
#
# @author Per-Henrik Kvalnes 2014
#

#
# The profile is connected to the user object
#
class UserProfile(models.Model):
    
    bio = models.CharField(max_length=400)
    user_ref = models.OneToOneField(User)
    image = models.FileField(upload_to="profileimg/%Y/%m")

#
# Defines one user skill
# A user can have many skills
#
class UserSkill(models.Model):
    skill = models.CharField(max_length=22)
    user = models.ForeignKey(User)

    # A user just have one skill of a same type
    class Meta:
        unique_together = ('skill', 'user')
#
# Lost password validation code
#
class PwdValidationCode(models.Model):

    def timedelta():
        return datetime.datetime.now() + datetime.timedelta(hours=2)

    code = models.CharField(max_length=40, unique=True)
    owner = models.ForeignKey(User)
    expire = models.DateTimeField(default=timedelta)

class UsrValidationCode(models.Model):

    def timedelta():
        return datetime.datetime.now() + datetime.timedelta(hours=2)

    def usrcode():
        time = datetime.datetime.now()
        code = time.year+time.day+time.minute+time.second
        code = sha.new(str(code)).hexdigest()
        return code

    code = models.CharField(max_length=40, unique=True, default=usrcode)
    owner = models.ForeignKey(User)
    expire = models.DateTimeField(default=timedelta)
