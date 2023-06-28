from django.db import models
from django.contrib.auth.models import User
from djongo.models.fields import ArrayField 
from .project import Project
from pymongo.errors import PyMongoError

class Task(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    date = models.DateField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(User, related_name='contributed_tasks')
    progression = models.IntegerField(default=0)
    project_id = models.CharField(max_length=100)
    description = models.TextField()
    datasets = models.JSONField()

    def insertTask(self):
        try:
            super().save()
        except PyMongoError as e:
            print(f"Create task fail: {str(e)}")
            return 0
        
        return 1