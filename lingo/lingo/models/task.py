from django.db import models
from djongo.models.fields import ArrayField 

class Task(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    date = models.DateField()
    asignee = models.CharField(max_length=50)
    contributor = models.JSONField()
    progression = models.IntegerField()
    project_id = models.CharField(max_length=50)
    description = models.TextField()
    datasets = models.JSONField()