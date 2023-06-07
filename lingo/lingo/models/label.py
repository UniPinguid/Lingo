from django.db import models
from djongo.models.fields import ArrayField 

class Label(models.Model):
    labelname = models.CharField(max_length=100)
    description = models.TextField()
    color = models.CharField(max_length=20)