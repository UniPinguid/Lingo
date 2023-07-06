from typing import Any
from django.db import models
from pymongo.errors import PyMongoError


class CusUser(models.Model):
    phone = models.fields.CharField(max_length=10)
    role = models.fields.CharField(max_length=50)

    def __init__(self, _phone, _role, *args, **kwargs):
        super(CusUser, self).__init__(*args, **kwargs)
        self.phone = _phone
        self.role= _role

    def addUser(self):
        mess = "Success"
        try:
            super.save()
            
        except PyMongoError as e:
            mess = "Add User failed. Error: " + str(e)
        return mess
    

    



