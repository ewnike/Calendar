# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.
class Users(models.Model):
    first_name= models.CharField(max_length=25)
    aka=models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    birthdate=models.DateField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Appointments(models.Model):
    task = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    time = models.DateTimeField('date_created')
    user = models.ForeignKey(Users, related_name = "user_appointments")
