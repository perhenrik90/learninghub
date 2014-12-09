from django.db import models

# Count times a tag is searched for
class TagCounter(models.Model):
    
    tag = models.CharField(max_length=100)
    counter = models.IntegerField(default=0)

