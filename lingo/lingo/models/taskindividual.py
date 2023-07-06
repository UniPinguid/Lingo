from django.db import models
from django.contrib.auth.models import User
from djongo.models.fields import ArrayField 
from .project import Project
from pymongo.errors import PyMongoError


class TaskIndividual(models.Model):
    # id = models.CharField(max_length=10)
    user = models.CharField(max_length=255)
    task = models.CharField(max_length=10)
    labeling = models.JSONField()
    time = models.DateField()
    revise = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
