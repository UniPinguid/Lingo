from django.db import models
from djongo.models.fields import ArrayField


class Project(models.Model):
    id = models.CharField(max_length=50)
    projectname = models.CharField(max_length=100)
    tags = ArrayField(models.CharField(max_length=50))
    description = models.TextField()
    color = models.CharField(max_length=20)
    visibility = models.CharField(max_length=20)
    member = ArrayField(models.CharField(max_length=50))
    datasets = ArrayField(
        models.DictField(
            tenhienthi=models.CharField(max_length=100),
            content=models.TextField(),
            time=models.CharField(max_length=50)
        )
    )


    