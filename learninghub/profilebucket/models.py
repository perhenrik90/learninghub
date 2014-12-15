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
    user = models.OneToOneField(User);
    image = models.ImageField(upload_to="profileimg/%Y/%m")

#
# Defines one user skill
# A user can have many skills
#
class UserSkill(models.Model):
    skill = models.CharField(max_length=22)
    user = models.ForeignKey(User)
