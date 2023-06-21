from django.db import models
from djongo.models.fields import ArrayField 

class Label(models.Model):
    labelname = models.CharField(max_length=100)
    description = models.TextField()
    color = models.CharField(max_length=20)


    def __init__(self, project_id, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.project_id = project_id
    def __str__(self):
        return self.labelname
    def getLabelList(proID):
        labels = Label.objects.filter(project_id=proID)
        return labels
