from django.db import models
from django.contrib.auth.models import User
from djongo.models.fields import ArrayField 
from .project import Project

class Task(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    date = models.DateField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(User, related_name='contributed_tasks')
    progression = models.IntegerField(default=0)
    project_id = models.ForeignKey(Project,on_delete=models.CASCADE, related_name='task_set')
    description = models.TextField()
    datasets = models.JSONField()