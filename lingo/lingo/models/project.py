from django.db import models
from django_mongodb_engine.fields import ArrayModelField


class Project(models.Model):
    id = models.CharField(max_length=50)
    projectname = models.CharField(max_length=100)
    tags = ArrayModelField(models.CharField(max_length=50))
    description = models.TextField()
    color = models.CharField(max_length=20)
    visibility = models.CharField(max_length=20)
    member = ArrayModelField(models.CharField(max_length=50))
    datasets = ArrayModelField(
        models.DictField(
            tenhienthi=models.CharField(max_length=100),
            content=models.TextField(),
            time=models.CharField(max_length=50)
        )
    )


    