from django.db import models
from django.contrib.auth.models import User  # user tablosunu çektim

# Create your models here.

class SnmpDevices(models.Model):
    Device_Ip = models.CharField(max_length=15)
    System_Description = models.CharField(max_length=1000)
    System_Contact = models.CharField(max_length=1000)
    System_Name = models.CharField(max_length=1000)
    System_Location = models.CharField(max_length=1000)
    Community = models.CharField(max_length=1000)
    User = models.ForeignKey(User, default=None, on_delete=models.CASCADE)  # foreign key