import json
from django.db import models
from djongo import models
from django.contrib.auth.models import User
from djongo.models.fields import ArrayField 
from .project import Project
from pymongo.errors import PyMongoError

class Dataset(models.Model):
    datasetid = models.IntegerField(primary_key=True)
    content = models.TextField()
    requirement = models.CharField(max_length=100)

class Task(models.Model):
    taskid = models.IntegerField()
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    date = models.DateField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(User, related_name='contributed_tasks')
    progression = models.IntegerField(default=0)
    project_id = models.CharField(max_length=100)
    description = models.TextField()
    member = models.TextField()
    datasets = models.JSONField(default=list)

    def insertTask(self):
        try:
            super().save()
        except PyMongoError as e:
            print(f"Create task fail: {str(e)}")
            return 0
        
        return 1
    